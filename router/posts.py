import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status, HTTPException, BackgroundTasks
from main.router.admin.models import PostInDb

from main.utils.socket import HandleMutiConnection

from main.utils.db import get_connection
import json
router = APIRouter(prefix="/posts", tags=["posts"])

socket = HandleMutiConnection()


async def update_views(post_key: str):
    pass



@router.get('/')
async def get_posts():
    db_connection = get_connection('blog')
    posts = db_connection.fetch()
    return {
        'posts': posts.items
    }
    
    


@router.get("/{post_key}")
async def get_post(post_key: str, background_tasks: BackgroundTasks):
    db_connection = get_connection('blog')
    post = db_connection.get(post_key)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    # get related post
    
    related_post = db_connection.fetch()
    post['related'] = list(filter(lambda x: x['key'] != post_key and set(x.get('tags', [])).intersection(set(post.get('tags', []))), related_post.items))
    
    background_tasks.add_task(update_views, post_key)
    return {
        'post': post
    }
