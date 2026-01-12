from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr
from typing_extensions import Annotated
from pydantic.functional_validators import AfterValidator

Password = Annotated[
    str,
    AfterValidator(lambda v: v if 8 <= len(v) <= 64 else ValueError("Password must be 8–64 characters"))
]

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: Password

class LoginRequest(BaseModel):
    username: str  # can be username OR email
    password: str

class PostCreate(BaseModel):
    title: str
    category_id: int

    # ✅ BOTH OPTIONAL
    blocks: Optional[List[Any]] = None
    content: Optional[str] = None

class PostUpdate(BaseModel):
    title: str
    content: str
    category_id: int
    blocks: Optional[List[Any]] = []

class CommentCreate(BaseModel):
    content: str

class CommentUpdate(BaseModel):
    content: str

