#
from fastapi import FastAPI, Depends

# from app.config import settings
from database import Base, engine
from core.user.routes import user_router

app = FastAPI()

app.include_router(user_router, prefix="/user")


Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}
