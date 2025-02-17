from typing import List, Optional
from pydantic import BaseModel

# Placeholder schemas for related models.
# Replace or expand these with the actual fields for each related model.
class SubjectOut(BaseModel):
    # Define subject fields as needed
    class Config:
        from_attributes= True

class StudentOut(BaseModel):
    # Define student fields as needed
    class Config:
        from_attributes= True

class DepartmentOut(BaseModel):
    # Define department fields as needed
    class Config:
        from_attributes= True

class TeacherOut(BaseModel):
    # Define teacher fields as needed
    class Config:
        from_attributes= True

# Base schema containing common fields for Group
class GroupBase(BaseModel):
    name: str
    department_id: int

# Schema used when creating a new Group
class GroupCreate(GroupBase):
    pass

# Schema used when updating an existing Group
class GroupUpdate(BaseModel):
    name: Optional[str] = None
    department_id: Optional[int] = None

# Schema used when reading Group data from the DB
class GroupOut(GroupBase):
    id: int
    subjects: List[SubjectOut] = []
    students: List[StudentOut] = []
    department: DepartmentOut
    teachers: List[TeacherOut] = []

    class Config:
        from_attributes= True
