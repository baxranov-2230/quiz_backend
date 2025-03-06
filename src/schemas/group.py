from typing import  Optional
from pydantic import BaseModel

class GroupBase(BaseModel):
    name: str
    faculty_id: int

    class Config:
        from_attributes = True


class GroupCreateRequest(GroupBase):
    class Config:
        from_attributes = True


class GroupCreateResponse(GroupBase):
    id: int

    class Config:
        from_attributes = True


class GroupUpdate(BaseModel):
    name: Optional[str] = None
    faculty_id: Optional[int] = None

    class Config:
        from_attributes = True