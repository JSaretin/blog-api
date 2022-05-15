import time
from os import environ
from typing import Optional

from fastapi import HTTPException, status, Header, Depends, Cookie, Request
from jose import JWTError, jwt
from main.router.admin.models import User
from main.utils.db import get_connection

secret_key = environ.get('SECRET_KEY', 'secret')

def get_now():
    return time.time()

async def get_current_user(token: Optional[str] = Cookie(None)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing")
    # split_token = token.split(' ')
    # if len(split_token) != 2:
    #     print(split_token)
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    # if split_token[0] != 'Bearer':
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    
    if payload['exp'] < get_now():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is expired")
    db_connection = get_connection('blog_authors')
    user = db_connection.get(payload['user_id'])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    return User(**user)
