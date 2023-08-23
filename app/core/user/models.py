"""
Файл содержит модель пользователя для приложения.
Модель представляет собой класс User, который имеет следующие атрибуты:

- name: строка, представляющая имя пользователя
- email: строка, представляющая адрес электронной почты пользователя
- hashed_password: строка, представляющая пароль пользователя
"""
import uuid
from datetime import datetime, timedelta

import bcrypt
import jwt
from app.config import get_settings
from app.database import Base
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class User(Base):
    """
    Класс пользователя, предоставляющий методы для хеширования пароля, проверки пароля и генерации токена.
    """

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)
    posts = relationship("Post", back_populates="author")

    def hash_password(self, password: str):
        """
        Хеширует пароль пользователя.

        Аргументы:
        password (str): Пароль пользователя.

        """

        self.hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt().decode("utf-8")
        )

    def verify_password(self, password: str):
        """
        Проверяет пароль пользователя.

        Аргументы:
        password (str): Пароль пользователя.

        Возвращает:
        bool: True, если пароль правильный, иначе False.
        """

        return bcrypt.checkpw(password.encode("utf-8"), self.hashed_password("utf-8"))

    def generate_token(self):
        """
        Генерирует токен для пользователя.

        Возвращает:
        str: Токен пользователя.
        """

        expiration = datetime.utcnow() + timedelta(hours=24)
        payload = {"sub": str(self.id), "exp": expiration}
        return jwt.encode(
            payload, str(get_settings().SECRET_KEY), algorithm="HS256"
        )  # maybe worong
