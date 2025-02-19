from fastapi import APIRouter, Depends
from src.model.question import Question
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.settings.base import get_db


router = APIRouter()



@router.delete("/")
async def delete_all_question(
    db : AsyncSession = Depends(get_db)
):
    question = await db.execute(select(Question))
    result = question.scalars().all()
    
    for question in result:
        await db.delete(question)


    await db.commit()
    return {"message": "Delete all error"} 