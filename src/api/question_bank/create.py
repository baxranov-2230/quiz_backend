from fastapi import APIRouter, Depends , HTTPException , status
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.base import get_db
from src.schemas.question import QuestionText
from src.model import Question, User
from src.auth.utils import get_current_user


router = APIRouter()

@router.post("/create-question-by-text")
async def create(
    question_item: QuestionText,
    user_info: User = Depends(get_current_user),
    db:AsyncSession = Depends(get_db)
    ):
    if user_info.role.value != "teacher" or user_info.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="You not teacher"
        )
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