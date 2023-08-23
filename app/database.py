from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import get_settings

# Создание движка для подключения к базе данных
settings = get_settings()

DB_URL = (
    f"postgresql://{settings.USER}:{settings.PASSWORD}"
    + f"@{settings.HOST}:5432/{settings.DB_NAME}"
)
print(DB_URL)
engine = create_engine(DB_URL)


# Создание сессии для работы с базой данных
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
# session = Session()

# Создание базового класса для моделей
Base = declarative_base()
