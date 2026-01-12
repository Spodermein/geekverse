from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Comment, Post
from routers.schemas import CommentCreate, CommentUpdate
from auth import get_current_user

router = APIRouter(prefix="/comments", tags=["Comments"])

# =========================
# ✅ CREATE COMMENT
# =========================
@router.post("/posts/{post_id}")
def create_comment(
    post_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = Comment(
        content=comment.content,
        post_id=post_id,
        user_id=current_user.id,
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment



# =========================
# 📄 GET COMMENTS (PUBLIC)
# =========================
@router.get("/posts/{post_id}")
def get_comments(post_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Comment)
        .filter(Comment.post_id == post_id)
        .order_by(Comment.id.desc())
        .all()
    )


# =========================
# 🗑️ DELETE COMMENT
# Admin → any
# User → own
# =========================
@router.delete("/{comment_id}")
@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # 🔑 THIS IS THE IMPORTANT LINE
    if current_user.role != "admin" and comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed",
        )

    db.delete(comment)
    db.commit()

    return {"message": "Comment deleted"}

# =========================
# ✏️ UPDATE COMMENT
# Admin → any
# User → own
# =========================
@router.put("/{comment_id}")
def update_comment(
    comment_id: int,
    comment: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if current_user.role != "admin" and db_comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed",
        )

    db_comment.content = comment["content"]
    db.commit()
    db.refresh(db_comment)

    return db_comment