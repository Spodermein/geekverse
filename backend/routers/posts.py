from fastapi import APIRouter, Depends, HTTPException,status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from database import SessionLocal
from database import get_db
import models
from models import Post, Category, User, Comment, Bookmark
from routers.schemas import PostCreate, PostUpdate
from auth import get_current_user, admin_required
from sqlalchemy import func
from fastapi import UploadFile, File, Form
import base64


router = APIRouter(prefix="/posts", tags=["Posts"])

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# 🔍 SEARCH POSTS (PUBLIC)
# =========================
@router.get("/search")
def search_posts(q: str, db: Session = Depends(get_db)):
    return (
        db.query(Post)
        .filter(
            or_(
                Post.title.ilike(f"%{q}%"),
                Post.content.ilike(f"%{q}%"),
            )
        )
        .all()
    )


# =========================
# 📄 GET ALL POSTS (PUBLIC)
# =========================
@router.get("/")
def get_posts(
    category_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = (
        db.query(Post)
        .options(
            joinedload(Post.author),
            joinedload(Post.category),
        )
    )

    if category_id is not None:
        query = query.filter(Post.category_id == category_id)

    return query.all()


# =========================
# 📄 GET SINGLE POST (PUBLIC)
# =========================
@router.get("/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = (
        db.query(Post)
        .options(
            joinedload(Post.author),
            joinedload(Post.category),
            joinedload(Post.comments).joinedload(Comment.user),
        )
        .filter(Post.id == post_id)
        .first()
    )

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post



# =========================
# ✍️ CREATE POST (ADMIN ONLY)
# =========================
@router.post("/")
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    admin: User = Depends(admin_required),
):
    # ✅ validate category using post.category_id
    category = (
        db.query(Category)
        .filter(Category.id == post.category_id)
        .first()
    )
    if not category:
        raise HTTPException(status_code=400, detail="Invalid category")

    new_post = Post(
        title=post.title,
        blocks=post.blocks,      # 🔥 block-based content
        content=post.content,    # legacy fallback
        user_id=admin.id,
        category_id=post.category_id,
        image=None,              # legacy field, unused now
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post



# =========================
# ✏️ UPDATE POST (ADMIN ONLY)
# =========================
@router.put("/{post_id}")
def update_post(
    post_id: int,
    post: PostUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required),
):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    db_post.title = post.title
    db_post.category_id = post.category_id
    db_post.blocks = post.blocks
    db_post.content = post.content or ""

    db.commit()
    db.refresh(db_post)

    return db_post

# =========================
# 🗑️ DELETE POST (ADMIN ONLY)
# =========================
@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(admin_required),
):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(db_post)
    db.commit()

    return {"message": "Post deleted successfully"}



@router.get("/featured")
def get_featured_posts(db: Session = Depends(get_db)):
    return db.query(Post).filter(Post.featured == True).all()


@router.put("/{post_id}/featured")
def toggle_featured(
    post_id: int,
    db: Session = Depends(get_db),
    admin = Depends(admin_required),
):
    post = (
    db.query(Post)
    .options(
        joinedload(Post.author),
        joinedload(Post.category),
    )
    .filter(Post.id == post_id)
    .first()
)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.featured = not post.featured
    db.commit()
    db.refresh(post)

    return post


