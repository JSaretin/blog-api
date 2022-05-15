from fastapi import APIRouter, BackgroundTasks, status, HTTPException, Depends, File, UploadFile
from fastapi.responses import StreamingResponse, FileResponse
from secrets import token_urlsafe
from main.router.admin.utils import get_current_user

from main.utils.db import get_drive

router = APIRouter(prefix="/images", tags=["images"])

async def get_upload_image(file: UploadFile = File(...), name: str = None):
    drive = get_drive()

    file = drive.put(name, file.file, content_type='image/png')




@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_user)])
async def upload_image(background_tasks: BackgroundTasks, file: UploadFile = File(...) ):
    name = token_urlsafe(16) + '.png'
    
    background_tasks.add_task(get_upload_image, file=file, name=name)
    
    return {
        'message': 'Image uploaded',
        'name': name
    }
