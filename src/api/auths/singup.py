from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  
from src.schemas.user import RegisterRequest
from src.settings.base import get_db  
from src.model.user import User, UserRole 
from src.model import Student, Teacher
from src.auth.utils import hash_password

router = APIRouter()

@router.post("/signup")
async def register(user_data: RegisterRequest, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(User).filter(User.username == user_data.username))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    
    new_user = User(
        username=user_data.username,
        hashed_password=await hash_password(user_data.password),
        disabled=True,
        role=user_data.role.value
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)


    new_profile = None
    if new_user.role.value == UserRole.student.value:
        new_profile = Student(user_id=new_user.id)
        print("Some things", new_profile)
    elif new_user.role.value == UserRole.teacher.value:
        new_profile = Teacher(user_id=new_user.id)
        
    print(new_profile)
    if new_profile is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role specified for profile creation"
        )

    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)

    return {"message": "User registered successfully", "profile_id": new_profile.user_id}
