from fastapi import FastAPI


class Server:
    __app: FastAPI

    def __init__(self, app: FastAPI):
        self.__app = app

    def get_app(self) -> FastAPI:
        return self.__app

    @staticmethod
    def __register_events(app):
        pass

    @staticmethod
    def __register_routes(app):
        pass
