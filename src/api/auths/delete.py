from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  
from src.settings.base import get_db  
from src.model.user import User

router = APIRouter()

@router.delete("/delete")
async def delete(user_id: int, db: AsyncSession = Depends(get_db)):
    
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.delete(user)
    await db.commit()
    return "delete"
