from pydantic import BaseModel
from typing import Optional

class GroupSubjectAssociationBase(BaseModel):
    group_id: int
    subject_id: int

    class Config:
        from_attributes = True

class GroupSubjectAssociationCreate(GroupSubjectAssociationBase):
    pass

class GroupSubjectAssociationCreateResponse(GroupSubjectAssociationBase):
    class Config:
        from_attributes = True

class GroupSubjectAssociationUpdate(BaseModel):
    group_id: Optional[int] = None
    subject_id: Optional[int] = None

    class Config:
        from_attributes = True
