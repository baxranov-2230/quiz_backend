from fastapi import APIRouter, Depends, UploadFile, File, Form
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.settings.base import get_db
from src.model.question import Question
import os
import shutil
from uuid import uuid4

router = APIRouter()

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True) 

def save_file(file: Optional[UploadFile]) -> Optional[str]:
  
    if not file or not file.filename:  
        return None  

    file_ext = file.filename.split(".")[-1]
    unique_filename = f"{uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return f"/static/{unique_filename}"

@router.post("/create-question-by-image")
async def create(
    question_id: int = Form(...),  
    option_a_image: Optional[UploadFile] = File(None),
    option_b_image: Optional[UploadFile] = File(None),
    option_c_image: Optional[UploadFile] = File(None),
    option_d_image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
):


    # Only process files if they exist
    image_urls = {
        "option_a_image": save_file(option_a_image) if option_a_image and option_a_image.filename else None,
        "option_b_image": save_file(option_b_image) if option_b_image and option_b_image.filename else None,
        "option_c_image": save_file(option_c_image) if option_c_image and option_c_image.filename else None,
        "option_d_image": save_file(option_d_image) if option_d_image and option_d_image.filename else None,
    }

    image_urls = {key: value for key, value in image_urls.items() if value}

    if not image_urls:
        return {"message": "No images uploaded"}

    question_result = await db.execute(select(Question).where(Question.id == question_id))
    result = question_result.scalars().first()

    if not result:
        return {"error": "Question not found"} 

 
    for key, value in image_urls.items():
        setattr(result, key, value)

    await db.commit()
    await db.refresh(result)

    return {
        "message": "Question updated successfully!",
        "question_id": result.id,
        "image_urls": image_urls,
    }
