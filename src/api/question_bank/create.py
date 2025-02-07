from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.base import get_db
from src.schemas.question import QuestionBase
from src.model.question import Question

router = APIRouter()

@router.post("/create-question")
async def create_question(
    question_item: QuestionBase, 
    db: AsyncSession = Depends(get_db)
):
    try:
        quiz = Question(**question_item.model_dump(exclude_unset=True))
        db.add(quiz)
        await db.commit()
        await db.refresh(quiz)
        return quiz
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
