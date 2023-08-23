from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import get_settings

# Создание движка для подключения к базе данных
settings = get_settings()

DB_URL = (
    f"postgresql://{settings.USER}:{settings.PASSWORD}"
    + f"@{settings.HOST}:5432/{settings.DB_NAME}"
)
print(DB_URL)
engine = create_engine(DB_URL)


# Создание сессии для работы с базой данных
Session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
session = Session()

# Создание базового класса для моделей
Base = declarative_base()
