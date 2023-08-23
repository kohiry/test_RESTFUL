"""Тесты для проекта."""

import httpx
import pytest


def test_connection():
    response = httpx.get("http://0.0.0.0:8000")
    assert response.status_code == 200
    assert response.text == '{"Hello":"World"}'


# def test_logout():
#     response = httpx.get("http://0.0.0.0:8000/logout")
#     assert response.json()["result"] == "ok"


# def delete(username: str):
#     """Test for delete data from database."""
#     url = "https://0.0.0.0:8000/delete"
#     data = {
#         "username": username,
#     }
#     response = httpx.get(url, params=data)
#     assert response.status_code == 200
#     assert response.josn()["status"] == "deleted"


# def test_register():
#     """Test for register data to database."""
#     url = "https://0.0.0.0:8000/register"
#     data = {
#         "username": "test1",
#         "password": "1234567890",
#     }
#     response = httpx.get(url, params=data)
#     assert response.status_code == 200
#     assert response.josn()["username"] == "test1"


# def test_login(username: str):
#     """Функция test_login.
#     Проверяет правильность введенных пользователем логина и пароля.
#     """
#     data = {"username": username}
#     response = httpx.post("https://0.0.0.0:8000/login", data=data)

#     # 2. Проверка перенаправления на страницу авторизации после выхода
#     # 3. Проверка отсутствия доступа к защищенным страницам после выхода
#     # 4. Проверка возможности входа в систему после выхода
#     assert response.status_code == 200
#     # 1. Проверка наличия кнопки для выхода из системы
