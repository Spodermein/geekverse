from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

from routers.users import router as users_router
from routers.posts import router as posts_router
from routers.categories import router as categories_router
from routers.comments import router as comments_router
from routers.auth_router import router as auth_router
from routers.bookmarks import router as bookmarks_router
import models
from database import engine, Base
from seed_categories import seed_categories

app = FastAPI(redirect_slashes=False)
security = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    seed_categories()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(categories_router)
app.include_router(posts_router)
app.include_router(comments_router)
app.include_router(bookmarks_router)
