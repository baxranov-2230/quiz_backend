from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.base import get_db
from src.CRUD.CRUDBase import CRUDBaseAsync
from sqlalchemy.future import select
from src.model import Teacher , Subject
from src.model.teacher_subject_association import teacher_subject_association
from src.schemas.teacher_subject_association import TeacherSubjectAssociationCreate
from collections import defaultdict
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

teacher_subject_router = APIRouter(
    tags=["Teacher Subject Association"]
)

main_crud = CRUDBaseAsync(teacher_subject_association)

@teacher_subject_router.post("/create_teacher_subject_association")
async def create_teacher_subject_association(
    teacher_subject_association: TeacherSubjectAssociationCreate,
    db: AsyncSession = Depends(get_db)    
):
    return await main_crud.insert_many_to_many(db, obj_in=teacher_subject_association)


@teacher_subject_router.get("/teacher_subject_associations")
async def get_teacher_subject_associations(db: AsyncSession = Depends(get_db)):
    stmt = select(Teacher.id, Teacher.first_name, Teacher.last_name, Subject.id, Subject.name).join(Teacher.subjects)
    
    result = await db.execute(stmt)
    rows = result.all()

    if not rows:
        return {"message": "No teacher-subject associations found."}

    teacher_dict = defaultdict(lambda: {"id": None, "name": None, "subjects": []})

    for teacher_id, first_name, last_name, subject_id, subject_name in rows:
        if teacher_dict[teacher_id]["id"] is None:
            teacher_dict[teacher_id]["id"] = teacher_id
            teacher_dict[teacher_id]["name"] = f"{first_name} {last_name}"

        teacher_dict[teacher_id]["subjects"].append({"id": subject_id, "name": subject_name})

    return list(teacher_dict.values())


@teacher_subject_router.get("/teacher/{teacher_id}/subjects")
async def get_teacher_subjects_by_id(
    teacher_id: int,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Teacher).where(Teacher.id == teacher_id).options(selectinload(Teacher.subjects))
    result = await db.execute(stmt)
    teacher = result.scalar_one_or_none()

    if not teacher:
        return {"error": "Teacher not found"}

    return {
        "id": teacher.id,
        "name": f"{teacher.first_name} {teacher.last_name}",
        "subjects": [{"id": subject.id, "name": subject.name} for subject in teacher.subjects]
    }


@teacher_subject_router.get("/subject/{subject_id}/teachers")
async def get_subject_teachers_by_id(
    subject_id: int,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Subject).where(Subject.id == subject_id).options(selectinload(Subject.teachers))
    result = await db.execute(stmt)
    subject = result.scalar_one_or_none()

    if not subject:
        return {"error": "Subject not found"}

    return {
        "id": subject.id,
        "name": subject.name,
        "teachers": [
            {"id": teacher.id, "name": f"{teacher.first_name} {teacher.last_name}"}
            for teacher in subject.teachers
        ]
    }

@teacher_subject_router.put("/teacher/{teacher_id}/subjects")
async def update_teacher_subjects(
    teacher_id: int,
    subject_ids: list[int],  # Expecting a list of subject IDs
    db: AsyncSession = Depends(get_db)
):
    # Fetch the teacher
    teacher = await db.get(Teacher, teacher_id)
    if not teacher:
        return {"error": "Teacher not found"}

    # Fetch subjects by provided IDs
    stmt = select(Subject).where(Subject.id.in_(subject_ids))
    result = await db.execute(stmt)
    subjects = result.scalars().all()

    if not subjects:
        return {"error": "No valid subjects found"}

    # Update the teacher-subject associations
    teacher.subjects = subjects  # This automatically removes old associations

    # Commit changes
    await db.commit()
    return {"message": "Teacher subjects updated successfully"}

@teacher_subject_router.delete("/teacher/{teacher_id}/subject/{subject_id}")
async def remove_subject_from_teacher(
    teacher_id: int,
    subject_id: int,
    db: AsyncSession = Depends(get_db)
):
    # Fetch the teacher
    teacher = await db.get(Teacher, teacher_id)
    if not teacher:
        return {"error": "Teacher not found"}

    # Fetch the subject
    subject = await db.get(Subject, subject_id)
    if not subject:
        return {"error": "Subject not found"}

    # Check if the subject is associated with the teacher
    if subject not in teacher.subjects:
        return {"error": "Subject is not associated with this teacher"}

    # Remove the subject from the teacher
    teacher.subjects.remove(subject)

    # Commit the changes
    await db.commit()
    return {"message": f"Subject {subject.name} removed from teacher {teacher.first_name} {teacher.last_name}"}

@teacher_subject_router.delete("/teacher/{teacher_id}/subjects")
async def clear_teacher_subjects(
    teacher_id: int,
    db: AsyncSession = Depends(get_db)
):
    # Fetch the teacher
    teacher = await db.get(Teacher, teacher_id)
    if not teacher:
        return {"error": "Teacher not found"}

    # Clear all subjects
    teacher.subjects = []

    # Commit the changes
    await db.commit()
    return {"message": f"All subjects removed from teacher {teacher.first_name} {teacher.last_name}"}
