from pydantic import BaseModel
from typing import Optional

class TeacherGroupAssociationBase(BaseModel):
    teacher_id: int
    group_id: int

    class Config:
        from_attributes = True

class TeacherGroupAssociationCreate(TeacherGroupAssociationBase):
    pass

class TeacherGroupAssociationCreateResponse(TeacherGroupAssociationBase):
    class Config:
        from_attributes = True

class TeacherGroupAssociationUpdate(BaseModel):
    teacher_id: Optional[int] = None
    group_id: Optional[int] = None

    class Config:
        from_attributes = True
