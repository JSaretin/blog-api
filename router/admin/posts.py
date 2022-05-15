from fastapi import APIRouter, Depends, status, HTTPException

from main.router.admin.utils import get_current_user, get_now

from .models import NewPost, PostInDb
from main.utils.db import get_connection


router = APIRouter(prefix="/posts", dependencies=[Depends(get_current_user)])



@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(post_form: NewPost):
    now = get_now()
    post_to_save= PostInDb(**post_form.dict(),
                           created_at=now, updated_at=now).dict()
    post_to_save.pop('key')
    db_connection = get_connection('blog')
    
    post = db_connection.put(post_to_save)
    return {
        'post': post
    }
    

@router.put("/{post_key}")
async def update_post(post_key: str, post_form: NewPost):
    db_connection = get_connection('blog')
    saved_post = db_connection.get(post_key)
    
    if not saved_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    
    saved_post.pop('key')
    saved_post.update(post_form.dict())
    db_connection.update(saved_post, post_key)
    
    return {
        'message': 'Post updated',
    }
    

@router.delete("/{post_key}")
async def delete_post(post_key: str):
    db_connection = get_connection('blog')
    saved_post = db_connection.get(post_key)
    if not saved_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    db_connection.delete(post_key)
    return {
        'message': 'Post deleted',
    }
