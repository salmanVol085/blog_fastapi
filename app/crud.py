# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas, auth
from typing import Optional

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed = auth.hash_password(user.password)
    db_user = models.User(name=user.name, email=user.email, password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user: return None
    if not auth.verify_password(password, user.password): return None
    return user

# Blog related
def create_blog(db: Session, author: models.User, blog_in: schemas.BlogCreate):
    blog = models.Blog(title=blog_in.title, content=blog_in.content, author=author)
    db.add(blog); db.commit(); db.refresh(blog)
    return blog

def update_blog(db: Session, blog: models.Blog, data: dict):
    for k, v in data.items():
        setattr(blog, k, v)
    db.add(blog); db.commit(); db.refresh(blog)
    return blog

def delete_blog(db: Session, blog: models.Blog):
    db.delete(blog); db.commit()

# Comments
def add_comment(db: Session, user: models.User, blog: models.Blog, content: str):
    c = models.Comment(content=content, user=user, blog=blog)
    db.add(c); db.commit(); db.refresh(c); return c

# Likes
def toggle_like(db: Session, user: models.User, blog: models.Blog):
    existing = db.query(models.Like).filter(models.Like.user_id==user.id, models.Like.blog_id==blog.id).first()
    if existing:
        db.delete(existing); db.commit(); return False
    l = models.Like(user=user, blog=blog); db.add(l); db.commit(); return True

# Share
def share_blog(db: Session, blog: models.Blog, recipient: models.User):
    existing = db.query(models.Shared).filter(models.Shared.blog_id==blog.id, models.Shared.recipient_id==recipient.id).first()
    if existing:
        return existing
    s = models.Shared(blog=blog, recipient=recipient)
    db.add(s); db.commit(); db.refresh(s)
    return s
