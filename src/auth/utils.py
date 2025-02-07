from datetime import datetime , timedelta
from sqlalchemy.orm import Session
from jose import JWTError , jwt
from fastapi import Depends , HTTPException , status
from src.settings.config import settings
from src.model.user import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from src.model.user import UserRole
from src.settings.base import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

pwd_context = CryptContext(schemes=["bcrypt"] , deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str , hashed_password: str):
    return pwd_context.verify(plain_password , hashed_password)


def create_access_token(data: dict , expires_delta : timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode , settings.SECRET_KEY , algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp" : expire})
    return jwt.encode(to_encode , settings.REFRESH_SECRET_KEY , algorithm=settings.ALGORITHM)
    
def verify_token(token: str , secret_key: str):
    print('HH', token)
    try:
        payload = jwt.decode(token , secret_key , algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as e:
        print('ERR', e)
        return None
    
def get_user(db: Session, username : str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str , password: str):
    user = get_user(db , username)
    if not user or not verify_password(password , user.hashed_password):
        return None
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token, settings.SECRET_KEY)
    

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = get_user(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


    
def get_user_role(required_role: UserRole):
    def role_dependency(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_dependency