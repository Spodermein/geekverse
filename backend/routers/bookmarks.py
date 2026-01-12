from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models import Bookmark, Post, User
from auth import get_current_user

router = APIRouter(prefix="/bookmarks", tags=["Bookmarks"])


#  Toggle bookmark
@router.post("/{post_id}")
def toggle_bookmark(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    existing = (
        db.query(Bookmark)
        .filter(
            Bookmark.user_id == current_user.id,
            Bookmark.post_id == post_id,
        )
        .first()
    )

    if existing:
        db.delete(existing)
        db.commit()
        return {"bookmarked": False}

    bookmark = Bookmark(
        user_id=current_user.id,
        post_id=post_id,
    )
    db.add(bookmark)
    db.commit()

    return {"bookmarked": True}


#  Get my bookmarks
@router.get("/me")
def get_my_bookmarks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bookmarks = (
        db.query(Bookmark)
        .options(joinedload(Bookmark.post).joinedload(Post.author))
        .filter(Bookmark.user_id == current_user.id)
        .order_by(Bookmark.created_at.desc())
        .all()
    )

    return [b.post for b in bookmarks]


#  Public user bookmarks
@router.get("/user/{username}")
def get_user_bookmarks(
    username: str,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    bookmarks = (
        db.query(Bookmark)
        .options(joinedload(Bookmark.post).joinedload(Post.author))
        .filter(Bookmark.user_id == user.id)
        .order_by(Bookmark.created_at.desc())
        .all()
    )

    return [b.post for b in bookmarks]


@router.get("/check/{post_id}")
def check_bookmark(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exists = (
        db.query(Bookmark)
        .filter(
            Bookmark.user_id == current_user.id,
            Bookmark.post_id == post_id,
        )
        .first()
        is not None
    )

    return {"bookmarked": exists}
