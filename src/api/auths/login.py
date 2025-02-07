from fastapi import APIRouter , Depends , Response , Request , HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from src.model import User , Teacher , Student
from src.settings.base import get_db
from src.auth.utils import authenticate_user , create_access_token, create_refresh_token, get_current_user
from datetime import timedelta
from src.settings.config import settings


router = APIRouter()

@router.post("/login")
def login(response : Response, form_data: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(get_db)):
    user = authenticate_user(db , form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username and password"
        )
    access_token = create_access_token({"sub": user.username}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_refresh_token({"sub": user.username}, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
    
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, samesite="lax", secure=True)
    
    
    user_info = get_current_user(access_token, db)
    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User info not found")
    
    if user_info.role.value == "student":
        student_info = db.query(Student).filter(Student.user_id == user_info.id).first()
        if not student_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        return {"access_token": access_token,"token_type":"bearer", "user_info" : student_info}

    elif user_info.role.value == "teacher":
        teacher_info = db.query(Teacher).filter(Teacher.user_id == user_info.id).first()
        if not teacher_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Teacher not found"
            )
        return {"access_token": access_token,"token_type":"bearer", "user_info" : teacher_info}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")