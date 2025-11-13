# app/models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    blogs = relationship("Blog", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")
    inbox = relationship("Shared", back_populates="recipient", cascade="all, delete-orphan")

class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    author = relationship("User", back_populates="blogs")

    comments = relationship("Comment", back_populates="blog", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="blog", cascade="all, delete-orphan")
    shared_with = relationship("Shared", back_populates="blog", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    blog_id = Column(Integer, ForeignKey("blogs.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="comments")
    blog = relationship("Blog", back_populates="comments")

class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    blog_id = Column(Integer, ForeignKey("blogs.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="likes")
    blog = relationship("Blog", back_populates="likes")
    __table_args__ = (UniqueConstraint('user_id', 'blog_id', name='uix_user_blog_like'),)

class Shared(Base):
    __tablename__ = "shared"
    id = Column(Integer, primary_key=True, index=True)
    blog_id = Column(Integer, ForeignKey("blogs.id", ondelete="CASCADE"))
    recipient_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    sent_at = Column(DateTime, default=datetime.utcnow)

    blog = relationship("Blog", back_populates="shared_with")
    recipient = relationship("User", back_populates="inbox")
    __table_args__ = (UniqueConstraint('blog_id', 'recipient_id', name='uix_blog_recipient'),)
