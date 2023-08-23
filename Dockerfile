FROM python:alpine

WORKDIR /app
COPY pyproject.toml /app/

RUN pip install --upgrade pip
RUN pip install poetry && poetry config virtualenvs.create false && poetry install
COPY . /app/
