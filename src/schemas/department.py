from pydantic import BaseModel, Field
from typing import Optional, List

class DepartmentBase(BaseModel):
    name: str = Field(..., max_length=100)
    faculty_id: int

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    faculty_id: Optional[int] = None