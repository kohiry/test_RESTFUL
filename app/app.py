from fastapi import Depends, FastAPI, HTTPException, Request

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import User, get_async_session, Post
from app.schemas import UserCreate, UserRead, PostUpdate
from app.users import auth_backend, current_active_user, fastapi_users

import redis

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded, _rate_limit_exceeded_handler
)  # app.add_middleware(SlowAPIMiddleware)

redis_db = redis.Redis(host="redis", port=6379)


app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@app.post("/tasks")
@limiter.limit("100/minute")
async def create_tasks(
    request: Request,
    title: str,
    description: str,
    user: User = Depends(current_active_user),
    user_db: AsyncSession = Depends(get_async_session),
):
    new_post = Post(
        title=title,
        content=description,
        owner_id=user.id,  # Здесь user должен быть вашим экземпляром User
    )
    user_db.add(new_post)

    # Завершите транзакцию и сохраните изменения
    await user_db.commit()

    # Кеширование созданного поста в Redis
    redis_key = f"post:{new_post.id}"
    post_data = {
        "id": new_post.id,
        "title": new_post.title,
        "content": new_post.content,
        "owner_id": new_post.owner_id,
    }
    try:
        redis_db.hmset(redis_key, post_data)
    except redis.exceptions.RedisError as e:
        raise redis.exceptions.RedisError(
            "An error occurred while caching post: " + str(e)
        )
    # Установка ограничения на длительность хранения ключа в секундах (например, 1 час)
    await redis_db.expire(redis_key, 3600)

    return {"message": f"Post: {new_post.title} created with {user.email}"}


@app.get("/tasks")
@limiter.limit("100/minute")
async def get_tasks(
    request: Request,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    stmt = select(Post).where(Post.owner_id == user.id)
    posts = await db.execute(stmt)
    return posts.scalars().all()


@app.get("/tasks/{task_id}")
@limiter.limit("100/minute")
async def get_task(
    request: Request,
    task_id: int,
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session),
):
    redis_key = f"post:{task_id}"
    post_data = await redis.hgetall(redis_key)

    if not post_data:
        # Если данные отсутствуют в кеше, попробуйте получить их из базы данных
        post = await db.get(Post, task_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        # Сохраните данные в кеше для будущего использования
        post_data = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "owner_id": post.owner_id,
        }
        await redis_db.hmset_dict(redis_key, post_data)
        await redis_db.expire(redis_key, 3600)  # Установите ограничение по времени
        return post

    return post_data


@app.put("/tasks/{task_id}")
@limiter.limit("100/minute")
async def update_task(
    request: Request,
    task_id: int,
    post_update: PostUpdate,
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session),
):
    post = await db.get(Post, task_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.title = post_update.title
    post.content = post_update.content
    await db.commit()

    return {"message": "Post updated successfully"}


@app.delete("/tasks/{task_id}")
@limiter.limit("100/minute")
async def delete_task(
    request: Request,
    task_id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    post = await db.get(Post, task_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    await db.delete(post)
    await db.commit()

    return {"message": "Post deleted successfully"}
