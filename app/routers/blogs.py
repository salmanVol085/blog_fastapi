# app/routers/blogs.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, deps, crud, models
from typing import List
from ..database import SessionLocal

router = APIRouter(prefix="/blogs", tags=["blogs"])

@router.post("/", response_model=schemas.BlogOut)
def create_blog(blog_in: schemas.BlogCreate, db: Session = Depends(deps.get_db), current_user = Depends(deps.get_current_user)):
    b = crud.create_blog(db, current_user, blog_in)
    # compute counts
    return enrich_blog(db, b)

@router.get("/{blog_id}", response_model=schemas.BlogOut)
def get_blog(blog_id: int, db: Session = Depends(deps.get_db)):
    b = db.query(models.Blog).filter(models.Blog.id==blog_id).first()
    if not b: raise HTTPException(404, "Blog not found")
    return enrich_blog(db, b)

@router.put("/{blog_id}", response_model=schemas.BlogOut)
def update(blog_id:int, blog_in: schemas.BlogCreate, db: Session = Depends(deps.get_db), current_user = Depends(deps.get_current_user)):
    b = db.query(models.Blog).filter(models.Blog.id==blog_id).first()
    if not b: raise HTTPException(404, "Blog not found")
    if b.author_id != current_user.id:
        raise HTTPException(403, "Not allowed")
    b = crud.update_blog(db, b, blog_in.dict())
    return enrich_blog(db, b)

@router.delete("/{blog_id}")
def delete(blog_id:int, db: Session = Depends(deps.get_db), current_user = Depends(deps.get_current_user)):
    b = db.query(models.Blog).filter(models.Blog.id==blog_id).first()
    if not b: raise HTTPException(404, "Blog not found")
    if b.author_id != current_user.id:
        raise HTTPException(403, "Not allowed")
    crud.delete_blog(db, b)
    return {"detail": "deleted"}

# share
@router.post("/{blog_id}/share")
def share(blog_id:int, recipient_email: str, db: Session = Depends(deps.get_db), current_user = Depends(deps.get_current_user)):
    b = db.query(models.Blog).filter(models.Blog.id==blog_id).first()
    if not b: raise HTTPException(404, "Blog not found")
    recipient = db.query(models.User).filter(models.User.email==recipient_email).first()
    if not recipient: raise HTTPException(404, "Recipient not found")
    s = crud.share_blog(db, b, recipient)
    return {"detail": "shared", "recipient_id": recipient.id}

# helper to enrich response
def enrich_blog(db: Session, blog: models.Blog):
    likes = db.query(models.Like).filter(models.Like.blog_id==blog.id).count()
    comments = db.query(models.Comment).filter(models.Comment.blog_id==blog.id).count()
    out = schemas.BlogOut.from_orm(blog)
    out.likes_count = likes
    out.comments_count = comments
    return out
