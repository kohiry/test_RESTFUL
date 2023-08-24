from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import User, get_async_session, Post
from schemas import UserCreate, UserRead, PostUpdate
from users import auth_backend, current_active_user, fastapi_users
from slowapi import Limiter
from slowapi.util import get_remote_address

# from fastapi_users.db import SQLAlchemyUserDatabase

app = FastAPI()
limiter = Limiter(key_func=get_remote_address, default_limits=["100 per minute"])

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@app.post("/tasks")
@limiter.limit("100 per minute")
async def create_tasks(
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
    return {"message": f"Post: {new_post.title} created with {user.email}"}


@app.get("/tasks")
@limiter.limit("100 per minute")
async def get_tasks(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    stmt = select(Post).where(Post.owner_id == user.id)
    posts = await db.execute(stmt)
    return posts.scalars().all()


@app.get("/tasks/{task_id}")
@limiter.limit("100 per minute")
async def get_task(
    task_id: int,
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session),
):
    post = await db.get(Post, task_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.put("/tasks/{task_id}")
@limiter.limit("100 per minute")
async def update_task(
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
@limiter.limit("100 per minute")
async def delete_task(
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
