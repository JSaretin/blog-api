from pydantic import BaseModel
from typing import List


class NewPost(BaseModel):
    preview: str
    title: str
    body: str
    tags: List[str] = []
    
class PostInDb(NewPost):
    key: str = None
    views:     int = 0
    likes:     int = 0
    created_at: float
    updated_at: float
    
    
class Comment(BaseModel):
    name: str
    email: str
    content: str
    post_key: str
    
    
    
class LoginForm(BaseModel):
    username: str
    password: str
    is_robot: bool = False
    grant_access: bool = False
    
    loginBowser: str = ""
    loginUserAgent: str = ""
    loginIp: str = ""
    loginCountry: str = ""
    loginCity: str = ""
    loginRegion: str = ""
    
    
class RegisterForm(BaseModel):
    name: str
    username: str
    email: str
    password: str
    confirm_password: str
    terms: bool = False
    is_robot: bool = False
    grant_access: bool = False
    

class User(BaseModel):
    key: str= None
    name: str
    username: str
    email: str
    password: str
    lastLogin: float = None
    access_id: str = None
    last_login_ip: str = None
    last_login_country: str = None
    last_login_city: str = None
    last_login_region: str = None
    created_at: float
    updated_at: float