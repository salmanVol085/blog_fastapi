# app/routers/likes.py
from fastapi import APIRouter, Depends, HTTPException
from .. import deps, crud, models
from sqlalchemy.orm import Session

router = APIRouter(prefix="/likes", tags=["likes"])

@router.post("/blogs/{blog_id}")
def like(blog_id:int, db: Session = Depends(deps.get_db), current_user = Depends(deps.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id==blog_id).first()
    if not blog: raise HTTPException(404, "Blog not found")
    liked = crud.toggle_like(db, current_user, blog)
    return {"liked": liked}
