from fastapi import APIRouter, Depends, HTTPException, status
from src.settings.base import get_db
from sqlalchemy.orm import Session
from src.model import Student , Teacher
from src.model.user import User

router = APIRouter()

@router.delete("/delete")
def delete(user_id: int , db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    db.delete(user)
    db.commit()
    return "delete"