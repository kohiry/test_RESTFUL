from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app import app

# Создание движка для подключения к базе данных
engine = create_engine("postgresql://user:password@host:port/dbname")

# Создание базового класса для моделей
Base = declarative_base()

# Создание сессии для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()
