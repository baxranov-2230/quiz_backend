from pydantic import BaseModel
from typing import Optional


class FacultyBase(BaseModel):
    name: str
    
class FacultyCreate(FacultyBase):
    pass
    
class FacultyUpdate(BaseModel):
    name : Optional[str] = None
    
    