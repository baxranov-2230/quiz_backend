from typing import Optional
from pydantic import BaseModel




class StudentBase(BaseModel):
    user_id: Optional[int] = None
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    patronymic: Optional[str] = None
    group_id: Optional[int] = None
    jshir: Optional[str] = None
    passport: Optional[str] = None

    class Config:
        from_attributes = True



class StudentCreate(StudentBase):
    
    class Config:
        from_attributes = True




class StudentUpdate(BaseModel):
    user_id: Optional[int] = None
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    patronymic: Optional[str] = None
    group_id: Optional[int] = None
    jshir: Optional[str] = None
    passport: Optional[str] = None

    class Config:
        from_attributes = True