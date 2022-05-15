import time

from bcrypt import checkpw, gensalt, hashpw
from secrets import token_hex
from fastapi import APIRouter, Depends, HTTPException, Header, status
from jose import JWTError, jwt
from main.router.admin.utils import get_now
from main.utils.db import get_connection

from .models import LoginForm, RegisterForm, User
from .utils import get_current_user, secret_key

router = APIRouter(prefix="/auth", tags=["auth"])



@router.post("/login")
async def login(login_form: LoginForm):
    db_connection = get_connection('blog_authors')
    if login_form.is_robot or login_form.grant_access:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login")
    author = db_connection.fetch({'username': login_form.username})
    if not author.count:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login")
    author = author.items[-1]
    if not checkpw(login_form.password.encode('utf-8'), author['password'].encode('utf-8')):
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login")
    
  
    created_at = get_now()
    max_age = 60 * 60 * 24 * 7
    expires_in = created_at + max_age
    
    
    user_id = author.pop('key')
    access_id = token_hex(16)
    
    
    new_token = jwt.encode({'user_id': user_id,'exp': expires_in}, secret_key, algorithm='HS256')
    refresh_token = jwt.encode({'salt': access_id, 'created_at': created_at, 'expires_in': expires_in}, secret_key, algorithm='HS256')
    
    author.update({'access_id': access_id, 'lastLogin': created_at})

    db_connection.update(author, user_id)
    
    return {
        'token': f'{new_token}',
        'expiresIn': expires_in,
        'maxAge': max_age,
        'refresh_token': refresh_token
    }
    
    
@router.post("/register")
async def register(register_form: RegisterForm):
    if register_form.is_robot or register_form.grant_access or register_form.terms:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid registration")
    db_connection = get_connection('blog_authors')
    user = db_connection.fetch([{'username':register_form.username}, {'email':register_form.email}])
    if user.count:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User already exists")
    now = get_now()
    register_dicts = register_form.dict()
    register_dicts['password'] =  hashpw(register_form.password.encode('utf-8'), gensalt())
    register_dicts['created_at'] = register_dicts['updated_at'] = now
    
    new_user = User(**register_dicts).dict()
    new_user.pop('key')
    db_connection.put(new_user)
    
    return {
        'message': 'Registration successful',
    }
    
    
@router.get('/me', dependencies=[Depends(get_current_user)], response_model=User, response_model_exclude=['password'])
async def get_get_user(current_user = Depends(get_current_user)):
    return current_user

@router.post('/generate-token')
async def generate_token(custom_token: str = Header(None)):
    refresh_token = custom_token
    db_connection = get_connection('blog_authors')
    try:
        payload = jwt.decode(refresh_token, secret_key, algorithms=['HS256'])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    
    user = db_connection.fetch({'access_id': payload['salt']})
    if not user.count:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")
    user = user.items[-1]
    
    created_at = get_now()
    max_age = 60 * 60 * 24 * 7
    expires_in = created_at + max_age
    
    
    user_id = user.pop('key')
    access_id = token_hex(16)
    
    
    new_token = jwt.encode({'user_id': user_id,'exp': expires_in}, secret_key, algorithm='HS256')
    refresh_token = jwt.encode({'salt': access_id, 'created_at': created_at, 'expires_in': expires_in}, secret_key, algorithm='HS256')
    
    user.update({'access_id': access_id, 'lastLogin': created_at})

    db_connection.update(user, user_id)
    
    return {
        'token': f'{new_token}',
        'expiresIn': expires_in,
        'maxAge': max_age,
        'refresh_token': refresh_token,
        'user': user
    }
    