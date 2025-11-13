# app/routers/comments.py
from fastapi import APIRouter, Depends, HTTPException
from .. import deps, crud, schemas, models
from sqlalchemy.orm import Session

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/blogs/{blog_id}", response_model=schemas.CommentOut)
def add_comment(blog_id:int, payload:schemas.CommentCreate, db: Session = Depends(deps.get_db), current_user = Depends(deps.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id==blog_id).first()
    if not blog: raise HTTPException(404, "Blog not found")
    c = crud.add_comment(db, current_user, blog, payload.content)
    return c
