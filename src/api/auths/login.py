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
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    # First, authenticate the user
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username and password"
        )
    
    # Check the user's disabled column:
    # According to your logic, if disabled is False then the user is active (already logged in)
    if user.disabled is False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already logged in"
        )
    
    # Otherwise, the user is inactive (disabled == True) and we can mark them as active.
    # Update the user instance accordingly.
    user.disabled = False
    await db.commit()        # Commit the change to the database
    await db.refresh(user)   # Refresh the instance to reflect the update

    # Create access and refresh tokens
    access_token = await create_access_token(
        {"sub": user.username},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = await create_refresh_token(
        {"sub": user.username},
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    # Set the refresh token as an HttpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        secure=True
    )

    # Get additional user info using the access token
    user_info = await get_current_user(access_token, db)
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User info not found"
        )

    # Depending on the role, fetch the corresponding Teacher or Student info
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
