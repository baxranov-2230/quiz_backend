from typing import List, Optional
from pydantic import BaseModel, ConfigDict

# Placeholder schemas for related models.
# Replace the example fields with the actual fields of your models.

class DepartmentOut(BaseModel):
    id: int
    name: str  # Example field

    model_config = ConfigDict(from_attributes=True)


class UserOut(BaseModel):
    id: int
    username: str  # Example field

    model_config = ConfigDict(from_attributes=True)


class SubjectOut(BaseModel):
    id: int
    title: str  # Example field

    model_config = ConfigDict(from_attributes=True)


class QuestionOut(BaseModel):
    id: int
    content: str  # Example field

    model_config = ConfigDict(from_attributes=True)


class GroupOut(BaseModel):
    id: int
    name: str  # Example field

    model_config = ConfigDict(from_attributes=True)


# Base schema for Teacher (shared fields for create/update)
class TeacherBase(BaseModel):
    user_id: Optional[int] = None
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    patronymic: Optional[str] = None
    department_id: Optional[int] = None
    jshir: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# Schema used when creating a new Teacher
class TeacherCreate(TeacherBase):
    pass


# Schema used when updating an existing Teacher
class TeacherUpdate(BaseModel):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    patronymic: Optional[str] = None
    department_id: Optional[int] = None
    jshir: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# Schema used for reading Teacher data (including nested relationships)
class TeacherOut(TeacherBase):
    id: int
    department: Optional[DepartmentOut] = None
    user: Optional[UserOut] = None
    subjects: List[SubjectOut] = []
    questions: List[QuestionOut] = []
    groups: List[GroupOut] = []

    model_config = ConfigDict(from_attributes=True)
