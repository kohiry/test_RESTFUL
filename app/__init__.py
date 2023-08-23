from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.configuration.server import Server
from app.pkg import models
from app.pkg.database import DATABASE_URL


def create_app(_=None) -> FastAPI:
    app = FastAPI()

    register_tortoise(
        app,
        db_url=DATABASE_URL,
        modules={"models": ["models"]},
        generate_schemas=True,
    )

    return Server(app).get_app()
