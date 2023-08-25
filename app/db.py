from typing import AsyncGenerator
from sqlalchemy import Column, ForeignKey, Integer, String
from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, relationship
import os
from sqlalchemy.dialects.postgresql import UUID

# Получение настроек для подключения к базе данных из переменных окружения
user = os.environ["USER"]
database = os.environ["DB_NAME"]
password = os.environ["PASSWORD"]
print(user, database, password)

# Формирование URL для подключения к базе данных
DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@postgres/{database}"
print(DATABASE_URL)


# Определение базового класса для ORM моделей
class Base(DeclarativeBase):
    pass


# Определение ORM модели для пользователей с использованием FastAPI Users
class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    # Определение отношения между пользователем и их постами
    posts = relationship("Post", back_populates="owner")


# Определение ORM модели для постов
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    owner = relationship("User", back_populates="posts")


# Создание асинхронного движка и сессии для работы с базой данных
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# Функция для создания таблиц в базе данных
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Функция для получения асинхронной сессии для работы с базой данных
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


# Функция для получения базы данных пользователей для FastAPI Users
async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
