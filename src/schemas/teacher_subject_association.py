from pydantic import BaseModel
from typing import Optional

class TeacherSubjectAssociationBase(BaseModel):
    teacher_id: int
    subject_id: int

    class Config:
        from_attributes = True

class TeacherSubjectAssociationCreate(TeacherSubjectAssociationBase):
    pass

class TeacherSubjectAssociationCreateResponse(TeacherSubjectAssociationBase):
    class Config:
        from_attributes = True

class TeacherSubjectAssociationUpdate(BaseModel):
    teacher_id: Optional[int] = None
    subject_id: Optional[int] = None

    class Config:
        from_attributes = True
