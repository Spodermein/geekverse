from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, Boolean,UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql import func
from sqlalchemy import JSON

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="user")

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="user")



class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    posts = relationship("Post", back_populates="category")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)

    # 🔹 OLD CONTENT (legacy posts)
    content = Column(Text, nullable=True)

    # 🔹 OLD SINGLE IMAGE (legacy posts)
    image = Column(Text, nullable=True)

    # 🔥 NEW BLOCK-BASED CONTENT
    blocks = Column(JSON, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    author = relationship("User", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

    created_at = Column(TIMESTAMP, server_default=func.now())
    featured = Column(Boolean, default=False)

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")



class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User")
    post = relationship("Post")

    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="unique_user_post_bookmark"),
    )
