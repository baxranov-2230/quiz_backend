from typing import Optional
from pydantic import BaseModel

class SubjectBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class SubjectCreateRequest(SubjectBase):
    class Config:
        from_attributes = True


class SubjectCreateResponse(SubjectBase):
    id: int

    class Config:
        from_attributes = True


class SubjectUpdate(BaseModel):
    name: Optional[str] = None

    class Config:
        from_attributes = True
