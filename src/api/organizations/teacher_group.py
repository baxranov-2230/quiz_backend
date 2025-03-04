from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.base import get_db
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from src.CRUD.CRUDBase import CRUDBaseAsync
from src.model import Teacher , Group
from src.model.teacher_group_association import teacher_group_association
from src.schemas.teacher_group_association import TeacherGroupAssociationCreate
from collections import defaultdict 

teacher_group_router = APIRouter(
    tags=["Teacher Group Association"]
)

main_crud = CRUDBaseAsync(teacher_group_association)

@teacher_group_router.post("/create_teacher_group_association")
async def create_teacher_group_association(
    teacher_group_association: TeacherGroupAssociationCreate,
    db: AsyncSession = Depends(get_db)    
):
    return await main_crud.insert_many_to_many(db, obj_in=teacher_group_association)

@teacher_group_router.get("/teacher_group_associations")
async def get_teacher_group_associations(db: AsyncSession = Depends(get_db)):
    stmt = select(Teacher.id, Teacher.first_name, Teacher.last_name, Group.id, Group.name).join(Teacher.groups)
    
    result = await db.execute(stmt)
    rows = result.all()

    if not rows:
        return {"message": "No teacher-group associations found."}

    teacher_dict = defaultdict(lambda: {"id": None, "name": None, "groups": []})

    for teacher_id, first_name, last_name, group_id, group_name in rows:
        if teacher_dict[teacher_id]["id"] is None:
            teacher_dict[teacher_id]["id"] = teacher_id
            teacher_dict[teacher_id]["name"] = f"{first_name} {last_name}"

        teacher_dict[teacher_id]["groups"].append({"id": group_id, "name": group_name})

    return list(teacher_dict.values())


@teacher_group_router.get("/teacher/{teacher_id}/groups")
async def get_teacher_groups_by_id(
    teacher_id: int,
    db: AsyncSession = Depends(get_db)
):
 
    stmt = select(Teacher).where(Teacher.id == teacher_id).options(selectinload(Teacher.groups))
    result = await db.execute(stmt)
    teacher = result.scalar_one_or_none()

    if not teacher:
        return {"error": "Teacher not found"}

    return {
        "id": teacher.id,
        "name": f"{teacher.first_name} {teacher.last_name}",
        "groups": [{"id": group.id, "name": group.name} for group in teacher.groups]
    }

@teacher_group_router.get("/group/{group_id}/teachers")
async def get_group_teachers_by_id(
    group_id: int,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Group).where(Group.id == group_id).options(selectinload(Group.teachers))
    result = await db.execute(stmt)
    group = result.scalar_one_or_none()

    if not group:
        return {"error": "Group not found"}

    return {
        "id": group.id,
        "name": group.name,
        "teachers": [
            {"id": teacher.id, "name": f"{teacher.first_name} {teacher.last_name}"}
            for teacher in group.teachers
        ]
    }


@teacher_group_router.put("/teacher/{teacher_id}/groups")
async def update_teacher_groups(
    teacher_id: int,
    group_ids: list[int],  # Expecting a list of group IDs
    db: AsyncSession = Depends(get_db)
):
    # Fetch the teacher
    teacher = await db.get(Teacher, teacher_id)
    if not teacher:
        return {"error": "Teacher not found"}

    # Fetch groups by provided IDs
    stmt = select(Group).where(Group.id.in_(group_ids))
    result = await db.execute(stmt)
    groups = result.scalars().all()

    if not groups:
        return {"error": "No valid groups found"}

    # Update the teacher-group associations
    teacher.groups = groups  # This automatically removes old associations

    # Commit changes
    await db.commit()
    return {"message": "Teacher groups updated successfully"}


@teacher_group_router.delete("/teacher/{teacher_id}/group/{group_id}")
async def remove_group_from_teacher(
    teacher_id: int,
    group_id: int,
    db: AsyncSession = Depends(get_db)
):
    # Fetch the teacher
    teacher = await db.get(Teacher, teacher_id)
    if not teacher:
        return {"error": "Teacher not found"}

    # Fetch the group
    group = await db.get(Group, group_id)
    if not group:
        return {"error": "Group not found"}

    # Check if the group is associated with the teacher
    if group not in teacher.groups:
        return {"error": "Group is not associated with this teacher"}

    # Remove the group from the teacher
    teacher.groups.remove(group)

    # Commit the changes
    await db.commit()
    return {"message": f"Group {group.name} removed from teacher {teacher.first_name} {teacher.last_name}"}


@teacher_group_router.delete("/teacher/{teacher_id}/groups")
async def clear_teacher_groups(
    teacher_id: int,
    db: AsyncSession = Depends(get_db)
):
    # Fetch the teacher
    teacher = await db.get(Teacher, teacher_id)
    if not teacher:
        return {"error": "Teacher not found"}

    # Clear all groups
    teacher.groups = []

    # Commit the changes
    await db.commit()
    return {"message": f"All groups removed from teacher {teacher.first_name} {teacher.last_name}"}
