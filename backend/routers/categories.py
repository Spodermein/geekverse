from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Category

router = APIRouter(tags=["Categories"])

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.id).all()