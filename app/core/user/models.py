import uuid
from datetime import datetime, time

import bcrypt
import jwt
from app.database import Base
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)
    posts = relationship("Post", back_populates="author")

    def hashed_password(self, password: str):
        self.hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt().decode("utf-8")
        )

    def verify_password(self, password: str):
        return bcrypt.checkpw(password.encode("utf-8"), self.hashed_password("utf-8"))

    def generate_token(self):
        expiration =
