from fastapi import Depends, FastAPI

from db import User
from schemas import UserCreate, UserRead
from users import auth_backend, current_active_user, fastapi_users

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@app.post("/tasks")
async def create_tasks(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
