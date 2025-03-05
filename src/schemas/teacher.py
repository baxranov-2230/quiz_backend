from typing import List, Optional
from pydantic import BaseModel, ConfigDict

# Placeholder schemas for related models.
# Replace the example fields with the actual fields of your models.


# Base schema for Teacher (shared fields for create/update)
class TeacherBase(BaseModel):
    user_id: Optional[int] = None
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    patronymic: Optional[str] = None
    department_id: Optional[int] = None
    jshir: Optional[str] = None

    class Config:
        from_attributes = True

class TeacherCreateRequest(TeacherBase):
    class Config:
        from_attributes = True

class TeacherCreateResponse(TeacherBase):
    id: int

    class Config:
        from_attributes = True


class TeacherUpdate(BaseModel):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    patronymic: Optional[str] = None
    department_id: Optional[int] = None
    jshir: Optional[str] = None

    class Config:
        from_attributes = True