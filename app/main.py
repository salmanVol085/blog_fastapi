# app/main.py
from fastapi import FastAPI
from .database import engine, Base
from .routers import users, blogs, comments, likes, feed
import os

Base.metadata.create_all(bind=engine)



app = FastAPI(title="Blog Backend with Argon2")
app.include_router(users.router)
app.include_router(blogs.router)
app.include_router(comments.router)
app.include_router(likes.router)
app.include_router(feed.router)

# simple root
@app.get("/")
def root():
    return {"message": "Blog API up"}


