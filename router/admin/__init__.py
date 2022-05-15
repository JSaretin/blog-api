from fastapi import APIRouter, status, HTTPException

# from .models import Post, PostInDb
from main.utils.db import get_connection
from . import posts, auth, images


router = APIRouter(prefix="/admin", tags=["admin"])
router.include_router(posts.router)
router.include_router(auth.router)
router.include_router(images.router)