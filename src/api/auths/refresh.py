from fastapi import APIRouter , Depends , Response , Request , HTTPException, status
from sqlalchemy.orm import Session
from src.settings.base import get_db
from src.auth.utils import create_access_token, verify_token , get_user
from datetime import timedelta
from src.settings.config import settings

router = APIRouter()

@router.post("/refresh")
def refresh_token(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No refresh token provided"
        )
    
    payload = verify_token(refresh_token, settings.REFRESH_SECRET_KEY)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    username = payload.get("sub")
    user = get_user(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    new_access_token = create_access_token({"sub": user.username}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    
    return {"access_token": new_access_token, "token_type": "bearer"}