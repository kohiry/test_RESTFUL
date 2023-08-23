import os

from app.pkg.models import UserDB, UserModel
from fastapi_users.db import TortoiseUserDatabase

user = os.getenv("USER")
database = os.getenv("DB_NAME")
host = os.getenv("HOST")
password = os.getenv("PASSWORD")

DATABASE_URL = f"postgres://{user}:{password}@{host}:5432/{database}"


async def get_user_db():
    yield TortoiseUserDatabase(UserDB, UserModel)


# import asyncio
# import os

# from tortoise import Tortoise, fields
# from tortoise.models import Model


# class User(Model):
#     id = fields.IntField(pk=True)
#     name = fields.CharField(max_length=255)
#     email = fields.CharField(max_length=255)
#     age = fields.IntField()


# async def init_db():
#     user = os.getenv("USER")
#     database = os.getenv("DB_NAME")
#     host = os.getenv("HOST")
#     password = os.getenv("PASSWORD")

#     print(user, database, host, password)

#     await Tortoise.init(
#         db_url=f"postgres://{user}:{password}@{host}:5432/{database}",
#         modules={"models": ["__main__"]},
#     )

#     await Tortoise.generate_schemas()


# # Создаем событийный цикл и запускаем асинхронную функцию init_db()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(init_db())
