from fastapi import APIRouter, Depends, HTTPException, UploadFile , File, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.base import get_db
from src.schemas.question import QuestionBase
from src.model.question import Question
import shutil
import os 
from uuid import uuid4

router = APIRouter()

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR , exist_ok=True)


async def save_file(file: UploadFile) -> str:
    if file:
        filename = f"{uuid4()}_{file.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return filepath  
    return None

@router.post("/create-question")
async def create_question(
    text: str = None,

    image: UploadFile = File(None),
    option_a: str = None,
    option_a_image: UploadFile = File(None),
    option_b: str = None,
    option_b_image: UploadFile = File(None),
    option_c: str = None,
    option_c_image: UploadFile = File(None),
    option_d: str = None,
    option_d_image: UploadFile = File(None),
    db: AsyncSession = Depends(get_db)
):
    try:
        quiz = Question(
            text=text,
            image=await save_file(image),
            option_a=option_a,
            option_a_image=await save_file(option_a_image),
            option_b=option_b,
            option_b_image=await save_file(option_b_image),
            option_c=option_c,
            option_c_image=await save_file(option_c_image),
            option_d=option_d,
            option_d_image=await save_file(option_d_image),
        )

        db.add(quiz)
        await db.commit()
        await db.refresh(quiz)
        return quiz
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

