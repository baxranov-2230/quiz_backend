import asyncio
from datetime import datetime, timedelta
from jose import JWTError, jwt, ExpiredSignatureError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.settings.config import settings
from src.model.user import User
from src.settings.base import get_db  
from typing import List , Callable
import secrets




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def hash_password(password: str) -> str:
    return await asyncio.to_thread(pwd_context.hash, password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return await asyncio.to_thread(pwd_context.verify, plain_password, hashed_password)


async def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    
    return await asyncio.to_thread(jwt.encode, to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def create_refresh_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return await asyncio.to_thread(jwt.encode, to_encode, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)


async def verify_token(token: str, secret_key: str):
    try:
        payload = await asyncio.to_thread(jwt.decode, token, secret_key, algorithms=[settings.ALGORITHM])
        return payload
    except ExpiredSignatureError:
        unverified_payload = jwt.get_unverified_claims(token)
        unverified_payload.setdefault("is_expired", True)
        return unverified_payload
    except JWTError:
        return None


async def get_user(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalar_one_or_none()


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user(db, username)
    if not user or not await verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: AsyncSession = Depends(get_db)
):
    payload = await verify_token(token, settings.SECRET_KEY)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    user = await get_user(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

def check_user_role(allowed_roles: List[str]) -> Callable:
    async def role_checker(user_info: User = Depends(get_current_user)) -> User:
        if user_info.role.value not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"You do not have permission. Allowed roles: {allowed_roles}",
            )
        return user_info  
    return role_checker 
    
    
async def generate_password():
    return secrets.token_hex(4)