from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  
from src.settings.base import get_db  
from src.model import User , Student, Teacher

router = APIRouter()

@router.delete("/delete/{user_id}")
async def delete(user_id: int, db: AsyncSession = Depends(get_db)):
    
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if user.role.value == "student":
        results = await db.execute(select(Student).where(Student.user_id == user_id))
        student = results.scalar_one_or_none()
        await db.delete(student)    
    if user.role.value == "teacher":
        results = await db.execute(select(Teacher).where(Teacher.user_id == user_id))
        teacher = results.scalar_one_or_none()
        await db.delete(teacher)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    await db.delete(user)
    await db.commit()
    return "delete"
