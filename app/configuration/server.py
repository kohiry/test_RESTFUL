from app.configuration.routes import __routes__
from fastapi import FastAPI


class Server:
    __app: FastAPI

    def __init__(self, app: FastAPI):
        self.__app = app
        self.__register_routes(app)

    def get_app(self) -> FastAPI:
        return self.__app

    @staticmethod
    def __register_events(app):
        # app.on_event('startup')(name func for event)
        pass

    @staticmethod
    def __register_routes(app):
        __routes__.register_routes(app)
