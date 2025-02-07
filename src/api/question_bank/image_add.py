from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.base import get_db
from pathlib import Path
from src.model.question import Question
import aiofiles

router = APIRouter()

UPLOAD_DIR = Path("uploaded_images")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.put("/upload/image/{id}")
async def upload_image(
    id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, 
            detail="File is not an image."
        )
    
    # Retrieve the question using its primary key.
    question = await db.get(Question, id)
    if not question:
        raise HTTPException(
            status_code=404, 
            detail="Question not found."
        )
    
    try:
        image_path = UPLOAD_DIR / file.filename
        
        # Asynchronously write the uploaded file to disk.
        async with aiofiles.open(image_path, "wb") as out_file:
            content = await file.read()  # Read the file contents asynchronously.
            await out_file.write(content)
        
        # Update the question with the path of the uploaded image.
        question.imgae = str(image_path)
        await db.commit()
        await db.refresh(question)
        
        return {
            "message": "Image added successfully",
            "question_id": question.id,
            "image_path": question.imgae,
        }
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to upload image: {str(e)}"
        )
