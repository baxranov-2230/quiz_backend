from fastapi import APIRouter , Response , Depends
from sqlalchemy.orm import Session
from src.settings.base import get_db
from src.auth.utils import get_current_user
from src.model import User

router = APIRouter()


@router.post("/logout")
def logout(
    response: Response , 
    user_id : User = Depends(get_current_user),
    db : Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id.id).first()
    user.disabled = True
    db.commit()
        
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}