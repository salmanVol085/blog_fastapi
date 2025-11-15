# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import users, blogs, comments, likes, feed
import os

Base.metadata.create_all(bind=engine)



app = FastAPI(title="Blog Backend with Argon2")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(blogs.router)
app.include_router(comments.router)
app.include_router(likes.router)
app.include_router(feed.router)

# simple root
@app.get("/")
def root():
    return {"message": "Blog API up"}


