from fastapi import APIRouter, status, HTTPException
from fastapi.responses import StreamingResponse
from main.utils.db import get_drive

router = APIRouter(prefix="/images")



@router.get("/{name}")
async def get_image(name: str):
    drive = get_drive()
    file = drive.get(name)
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    
    return StreamingResponse(file.iter_chunks(1024), media_type='image/png')

