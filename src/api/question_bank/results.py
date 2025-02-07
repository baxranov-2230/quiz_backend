from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.settings.base import get_db
from src.model import Question, Student, User
from src.auth.utils import get_current_user

router = APIRouter()

@router.get("/test-check")
async def check_test(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    
    result = await db.execute(select(Student).filter(Student.id == user.id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="User not found")

    
    if not student.quiz_result or not isinstance(student.quiz_result, dict):
        raise HTTPException(status_code=400, detail="Invalid or missing quiz result")

    quiz_result = student.quiz_result
    question_texts = list(quiz_result.keys())

    
    result = await db.execute(select(Question).where(Question.text.in_(question_texts)))
    questions_list = result.scalars().all()

    questions = {q.text: q.A for q in questions_list}

    
    correct_count = sum(1 for q_text, answer in quiz_result.items() if questions.get(q_text) == answer)
    incorrect_count = len(quiz_result) - correct_count


    student.correct_answers = correct_count
    student.incorrect_answers = incorrect_count

    await db.commit()
    await db.refresh(student)
    return student
