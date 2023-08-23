from app.core.user.models import User
from app.core.user.schema import Token, UserCreate, UserLogin
from app.dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

user_router = APIRouter()


@user_router.post("/signup")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    user = User(username=user_data.username, email=user_data.email)
    user.hash_password(user_data.password)
    db.add(user)
    db.comit()
    return {"message": "User created"}


@user_router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if user is None or not user.verify_password(user_data.password):
        raise HTTPException(status_code=401, default="Invalid Credentials")
    token = user.generate_token()
    return Token(access_token=token, token_type="bearer")
