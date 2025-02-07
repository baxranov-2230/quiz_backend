from pydantic import BaseModel, EmailStr
from src.model.user import UserRole

class UserResponse(BaseModel):
    username: str
    disabled: bool
    role: UserRole
    
class RegisterRequest(BaseModel):
    username: str
    password: str
    role : UserRole
    
class StudentUpdate(BaseModel):
    last_name : str 
    first_name: str
    
class TeacherUpdate(BaseModel):
    last_name : str 
    first_name: str