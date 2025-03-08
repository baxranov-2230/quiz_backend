from fastapi import APIRouter
from .faculty import faculty_router as faculty
from .department import department_router as department
from .group import group_router as group
from .student import student_router as student
from .teacher import teacher_router as teacher
from .subject import subject_router as subject
from .teacher_group import teacher_group_router as teacher_group
from .teacher_subject import teacher_subject_router as teacher_subject


organization_router = APIRouter()


organization_router.include_router(faculty)
organization_router.include_router(department)
organization_router.include_router(group)
organization_router.include_router(student)
organization_router.include_router(teacher)
organization_router.include_router(subject)
organization_router.include_router(teacher_group)
organization_router.include_router(teacher_subject)

