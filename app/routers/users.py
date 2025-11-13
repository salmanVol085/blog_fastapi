# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, crud, deps, auth


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(deps.get_db)):
    return crud.create_user(db, user)


@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(deps.get_db)):
    user = crud.get_user_by_email(db, form.username)
    if not user or not auth.verify_password(form.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # for create access token
    token = auth.create_access_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}
    
@router.get("/me", response_model=schemas.UserOut)
def me(current_user=Depends(deps.get_current_user)):
    return current_user
