from fastapi import APIRouter
from .department import department_router as department
from .faculty import faculty_router as faculty
from .group import group_router as group
from .student import student_router as student
from .teacher import teacher_router as teacher


organization_router = APIRouter()

organization_router.include_router(department)
organization_router.include_router(faculty)
organization_router.include_router(group)
organization_router.include_router(student)
organization_router.include_router(teacher)

