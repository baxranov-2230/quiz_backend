from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.base import get_db
from src.schemas.question import QuestionUpdate
from src.model import Question , User
from src.auth.utils import get_current_user


router = APIRouter()

@router.put("/update-question")
async def update_question(
    question_id: int,
    question_item: QuestionUpdate,
    user_data: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if user_data.role.value == "teacher" or user_data.role.value == "admin":
        question = await db.get(Question, question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        

        update_data = question_item.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(question, key, value)
        

        await db.commit()
        await db.refresh(question)
        return question
