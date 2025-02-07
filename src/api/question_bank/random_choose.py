from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.model.question import Question
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
        variants = [question.A, question.B, question.C, question.D]
        random.shuffle(variants)
        question.A, question.B, question.C, question.D = variants
    
    response = [
        QuestionResponse(**{k: v for k, v in question.__dict__.items() if not k.startswith('_')})
        for question in random_questions
    ]
    
    return response
