from typing import List, Optional
from pydantic import BaseModel, ConfigDict

# Placeholder schemas for nested models. Update fields as necessary.
class GroupOut(BaseModel):
    id: int
    name: str  # Example field

    model_config = ConfigDict(from_attributes=True)


class ResultStudentOut(BaseModel):
    id: int
    score: float  # Example field; update with actual fields

    model_config = ConfigDict(from_attributes=True)


class UserOut(BaseModel):
    id: int
    username: str  # Example field; update with actual fields

    model_config = ConfigDict(from_attributes=True)


# Base schema containing common fields for Student
class StudentBase(BaseModel):
    user_id: Optional[int] = None
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    patronymic: Optional[str] = None
    group_id: Optional[int] = None
    jshir: Optional[str] = None
    passport: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# Schema used when creating a new Student
class StudentCreate(StudentBase):
    pass


# Schema used when updating an existing Student
class StudentUpdate(BaseModel):
    user_id: Optional[int] = None
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    patronymic: Optional[str] = None
    group_id: Optional[int] = None
    jshir: Optional[str] = None
    passport: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# Schema used for reading Student data (including nested relationships)
class StudentOut(StudentBase):
    id: int
    group: Optional[GroupOut] = None
    results: List[ResultStudentOut] = []
    user: Optional[UserOut] = None

    model_config = ConfigDict(from_attributes=True)
