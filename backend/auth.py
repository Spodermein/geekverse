from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import SessionLocal
import models

# =====================
# CONFIG
# =====================
SECRET_KEY = "Thegamingbeaver198"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# =====================
# PASSWORD UTILS
# =====================
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# =====================
# JWT UTILS
# =====================
def create_access_token(data: dict):
    to_encode = data.copy()
    # 🔒 JWT best practice: sub MUST be string
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# =====================
# DB DEPENDENCY
# =====================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =====================
# AUTH DEPENDENCY
# =====================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


# =====================
# ADMIN GUARD
# =====================
def admin_required(current_user = Depends(get_current_user)):
    print("ADMIN CHECK →", current_user.id, current_user.username, current_user.role)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return current_user
