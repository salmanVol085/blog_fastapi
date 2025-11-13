from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models, auth


oauth2 = OAuth2PasswordBearer(tokenUrl="/users/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2), db: Session = Depends(get_db)):
    payload = auth.decode_token(token)
    user = db.query(models.User).filter(models.User.id == payload.get("user_id")).first()
    return user
