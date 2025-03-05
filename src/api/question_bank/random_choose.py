from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.model import Question, UserRole
from src.settings.base import get_db
from src.schemas.question import QuestionResponse
from typing import List
import random

router = APIRouter()

@router.get("/random-choose", response_model=List[QuestionResponse])
async def get_test(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Question))
    db_content = result.scalars().all()

    if not db_content:
        raise HTTPException(status_code=404, detail="No questions available")

    num_questions_to_select = min(25, len(db_content))
    random_questions = random.sample(db_content, num_questions_to_select)

    for question in random_questions:
        variants = [question.option_a, question.option_b, question.option_c, question.option_d]
        random.shuffle(variants)
        question.option_a, question.option_b, question.option_c, question.option_d = variants

    response = [QuestionResponse(**question.__dict__) for question in random_questions]
    return response
