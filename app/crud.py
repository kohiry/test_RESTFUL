from sqlalchemy.orm import Session

from . import models, schemas


def get_post(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()


def create_user_post(db: Session, item: schemas.PostCreate, user_id: int):
    db_post = models.Post(**item.dict(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post
