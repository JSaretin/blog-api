from fastapi import  FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import admin, posts, images


app = FastAPI(prefix="/api")

cors_origins = ['*']

app.add_middleware( CORSMiddleware, 
                   allow_origins=cors_origins, 
                   allow_credentials=True, 
                   allow_methods=["*"], allow_headers=["*"])


app.include_router(admin.router)
app.include_router(posts.router)
app.include_router(images.router)


