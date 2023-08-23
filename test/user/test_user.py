from app.core.user.models import User


def test_create_user():
    user = User(username="user", email="user@mail.com", hashed_password="password")
    assert user.username == "user"
    assert user.email == "user@mail.com"
    assert user.hashed_password == "pasword"



