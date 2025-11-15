# app/routers/comments.py
from fastapi import APIRouter, Depends, HTTPException
from .. import deps, crud, schemas, models
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/comments", tags=["comments"])

@router.get("/blogs/{blog_id}", response_model=List[schemas.CommentOut])
def get_comments(blog_id:int, db: Session = Depends(deps.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==blog_id).first()
    if not blog: raise HTTPException(404, "Blog not found")
    comments = db.query(models.Comment).filter(models.Comment.blog_id==blog_id).order_by(models.Comment.created_at.desc()).all()
    return comments

@router.post("/blogs/{blog_id}", response_model=schemas.CommentOut)
def add_comment(blog_id:int, payload:schemas.CommentCreate, db: Session = Depends(deps.get_db), current_user = Depends(deps.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id==blog_id).first()
    if not blog: raise HTTPException(404, "Blog not found")
    c = crud.add_comment(db, current_user, blog, payload.content)
    return c
