
import json
from fastapi import HTTPException, WebSocket, status
from .db import get_connection
from .socket import HandleMutiConnection


async def get_related_post(post_key: str, websocket: WebSocket, socket: HandleMutiConnection):
    db_connection = get_connection('blog')
    post = db_connection.get(post_key)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    tags = post.get('tags', [])
    posts = db_connection.fetch()
    
    for post in posts.items:
        if post['key'] == post_key:
            continue
        is_related = len([tag for tag in post.get('tags') if tag in tags])
        if is_related:
            await socket.send_data(websocket, json.dumps({'related': True, 'post': post, 'related_to': post_key}))