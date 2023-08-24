from typing import AsyncGenerator
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
import os
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

user = os.getenv("USER")
database = os.getenv("DB_NAME")
host = os.getenv("HOST")
password = os.getenv("PASSWORD")

DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}:5432/{database}"


class base(DeclarativeBase):
    pass


Base = base()


class User(SQLAlchemyBaseUserTableUUID, base):
    items = relationship("User", back_populates="posts")


from sqlalchemy import Column, Integer, String, DateTime


class Post(base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    owner = relationship("Post", back_populates="owner")


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
