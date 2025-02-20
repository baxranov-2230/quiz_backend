from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.base import get_db
from src.schemas.question import QuestionText
from src.model.question import Question


router = APIRouter()

@router.post("/create-question-by-text")
async def create(
    question_item: QuestionText,
    db:AsyncSession = Depends(get_db)
    ):
    
    new_question = Question(
        text = question_item.text,
        option_a = question_item.option_a,
        option_b = question_item.option_b,
        option_c = question_item.option_c,
        option_d = question_item.option_d
    )
    
    db.add(new_question)
    await db.commit()
    await db.refresh(new_question)
    return {
        "text" : new_question.text,
        "option_a": new_question.option_a,
        "option_b": new_question.option_b,
        "option_c": new_question.option_c,
        "option_d": new_question.option_d,
    }