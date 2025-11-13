# app/routers/feed.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import deps, models, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/feed", tags=["feed"])

@router.get("/", response_model=list[schemas.BlogOut])
def feed(db: Session = Depends(deps.get_db)):
    # simple recent feed: last 50 blogs
    blogs = db.query(models.Blog).order_by(models.Blog.created_at.desc()).limit(50).all()
    result=[]
    for b in blogs:
        likes = db.query(models.Like).filter(models.Like.blog_id==b.id).count()
        comments = db.query(models.Comment).filter(models.Comment.blog_id==b.id).count()
        o = schemas.BlogOut.from_orm(b)
        o.likes_count = likes
        o.comments_count = comments
        result.append(o)
    return result
