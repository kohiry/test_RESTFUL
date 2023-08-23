from app.core.post.models import Post
from app.core.user.models import User


def test_create_post():
    post = Post(title="my first post", content="this is my post")
    assert post.title == "my first post"
    assert post.content == "this is my post"


def test_user_posts_relationship():
    user = User(username="user", email="user@mail.com", hashed_password="password")
    post = Post(title="my first post", content="this is my post", author=user)
    assert post.author == user
