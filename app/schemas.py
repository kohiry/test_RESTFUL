import uuid
from pydantic import BaseModel
from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    """Схема для чтения информации о пользователе.

    Наследует схему `BaseUser` от FastAPI Users и использует UUID в качестве идентификатора пользователя.
    """


class UserCreate(schemas.BaseUserCreate):
    """Схема для создания нового пользователя.

    Наследует схему `BaseUserCreate` от FastAPI Users для определения обязательных полей при регистрации.
    """


class UserUpdate(schemas.BaseUserUpdate):
    """Схема для обновления информации о пользователе.

    Наследует схему `BaseUserUpdate` от FastAPI Users для определения полей, которые можно обновить.
    """


class PostBase(BaseModel):
    """Базовая схема для создания и чтения информации о посте.

    Содержит поля, необходимые для создания поста: заголовок и описание.
    """


class PostCreate(PostBase):
    """Схема для создания нового поста.

    Наследует базовую схему `PostBase` и добавляет возможность указать дополнительные поля для создания.
    """

    title: str
    content: str


class PostUpdate(PostBase):
    title: str
    content: str
