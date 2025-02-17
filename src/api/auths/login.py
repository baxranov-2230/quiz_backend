from fastapi import APIRouter, Depends, Response, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  
from datetime import timedelta

from src.model import User, Teacher, Student
from src.settings.base import get_db  
from src.auth.utils import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_current_user,
)
from src.settings.config import settings

router = APIRouter()

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):

    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username and password"
        )

    if user.disabled is False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already logged in"
        )
    

    user.disabled = False
    await db.commit()        
    await db.refresh(user)   


    access_token = await create_access_token(
        {"sub": user.username},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = await create_refresh_token(
        {"sub": user.username},
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )


    user_info = await get_current_user(access_token, db)
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User info not found"
        )

    if user_info.role.value == "student":
        result = await db.execute(
            select(Student).filter(Student.user_id == user_info.id)
        )
        student_info = result.scalar_one_or_none()
        if not student_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_info": student_info
        }
    elif user_info.role.value == "teacher":
        result = await db.execute(
            select(Teacher).filter(Teacher.user_id == user_info.id)
        )
        teacher_info = result.scalar_one_or_none()
        if not teacher_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Teacher not found"
            )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_info": teacher_info
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role"
        )
