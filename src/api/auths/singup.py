from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.schemas.user import RegisterRequest
from src.settings.base import get_db
from src.model.user import User, UserRole 
from src.model import Student, Teacher
from src.auth.utils import hash_password

router = APIRouter()

@router.post("/singup")
def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    new_user = User(
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
        disabled=False,
        role=user_data.role.value 
    )
    

        
    db.add(new_user)
    db.commit() 
    db.refresh(new_user)


    new_profile = None
    
    if new_user.role.value == UserRole.student.value:
        new_profile = Student(user_id=new_user.id)
    elif new_user.role.value == UserRole.teacher.value:
        new_profile = Teacher(user_id=new_user.id)
        

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return {"message": "User registered successfully", "profile_id": new_profile.user_id}
