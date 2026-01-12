from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from database import get_db
from models import User
from routers.schemas import RegisterRequest
from auth import hash_password, get_current_user

router = APIRouter(prefix="/users", tags=["Users"])



@router.get("/me")
def get_current_user_profile(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role,
    }


@router.get("/{username}")
def get_user_by_username(
    username: str,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
    }

