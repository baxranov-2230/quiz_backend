from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.base import get_db
from sqlalchemy.future import select
from src.model import Group , Subject
from src.CRUD.CRUDBase import CRUDBaseAsync
from src.model.group_subject_association import group_subject_association
from src.schemas.group_subject_association import (
    GroupSubjectAssociationCreate,
)
from sqlalchemy import insert  
from collections import defaultdict
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

group_subject_router = APIRouter(
    tags=["Group Subject Association"]
)

main_crud = CRUDBaseAsync(group_subject_association)

@group_subject_router.post("/create_group_subject_association")
async def create_group_subject_association(
    group_subject_association: GroupSubjectAssociationCreate,
    db: AsyncSession = Depends(get_db)    
):
    return await main_crud.insert_many_to_many(db, obj_in=group_subject_association)




@group_subject_router.get("/group_subject_association_get_all")
async def get_group_subject_associations(
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Group.id, Group.name, Subject.id, Subject.name).join(Group.subjects)
    
    result = await db.execute(stmt)
    rows = result.all()

    if not rows:
        return {"message": "No group-subject associations found."}

    group_dict = defaultdict(lambda: {"id": None, "name": None, "subjects": []})

    for group_id, group_name, subject_id, subject_name in rows:
        if group_dict[group_id]["id"] is None:
            group_dict[group_id]["id"] = group_id
            group_dict[group_id]["name"] = group_name

        group_dict[group_id]["subjects"].append({"id": subject_id, "name": subject_name})

    return list(group_dict.values())





@group_subject_router.get("/group_subject_association_get/{group_id}")
async def get_group_subject_association_by_id(
    group_id: int,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Group, Subject).join(Group.subjects).where(Group.id == group_id)
    
    result = await db.execute(stmt)
    rows = result.all()

    if not rows:
        return {"message": "Group not found or no subjects assigned"}

    group = rows[0][0]  

    return {
        "id": group.id,
        "name": group.name,
        "subjects": [{"id": subject.id, "name": subject.name} for _, subject in rows]
    }


@group_subject_router.get("/subject/{subject_id}/groups")
async def get_subject_groups_by_id(
    subject_id: int,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Subject).where(Subject.id == subject_id).options(selectinload(Subject.groups))
    result = await db.execute(stmt)
    subject = result.scalar_one_or_none()

    if not subject:
        return {"error": "Subject not found"}

    return {
        "id": subject.id,
        "name": subject.name,
        "groups": [
            {"id": group.id, "name": group.name}
            for group in subject.groups
        ]
    }



@group_subject_router.post("/group_subject_association_create/{subject_id}")
async def create_group_subject_association(
    subject_id: int,
    group_ids: list[int],
    db: AsyncSession = Depends(get_db),
):
    try:
        subject = await db.get(Subject, subject_id)
        if not subject:
            return {"error": "Subject not found"}
        
        # Fetch existing associations
        existing_stmt = select(group_subject_association.c.group_id).where(
            group_subject_association.c.subject_id == subject_id
        )
        existing_result = await db.execute(existing_stmt)
        existing_group_ids = set(existing_result.scalars().all())

        # Filter out already associated groups
        new_group_ids = [gid for gid in group_ids if gid not in existing_group_ids]
        
        if not new_group_ids:
            return {"message": "All groups are already associated with this subject"}

        # Insert new associations
        insert_stmt = insert(group_subject_association).values(
            [{"group_id": gid, "subject_id": subject_id} for gid in new_group_ids]
        )
        await db.execute(insert_stmt)
        await db.commit()

        return {"message": "Groups successfully associated with the subject"}

    except IntegrityError:
        await db.rollback()
        return {"error": "Duplicate entry detected"}
    
    except NoResultFound:
        return {"error": "Invalid data provided"}


@group_subject_router.put("/group_subject_association_update/{group_id}")
async def update_group_subject_association(
    group_id: int,
    subject_ids: list[int],
    db: AsyncSession = Depends(get_db)
):
    try:
        # Fetch the group
        group = await db.get(Group, group_id)
        if not group:
            return {"error": "Group not found"}


        stmt = select(Subject).where(Subject.id.in_(subject_ids))
        result = await db.execute(stmt)
        subjects = result.scalars().all()

        if not subjects:
            return {"error": "No valid subjects found"}


        group.subjects = subjects 


        await db.commit()
        return {"message": "Group subjects updated successfully"}

    except NoResultFound:
        return {"error": "Invalid data provided"}



@group_subject_router.delete("/group_subject_association_delete/{group_id}/{subject_id}")
async def remove_subject_from_group(
    group_id: int,
    subject_id: int,
    db: AsyncSession = Depends(get_db)
):

    group = await db.get(Group, group_id)
    if not group:
        return {"error": "Group not found"}


    subject = await db.get(Subject, subject_id)
    if not subject:
        return {"error": "Subject not found"}

    if subject not in group.subjects:
        return {"error": "Subject is not associated with this group"}


    group.subjects.remove(subject)

    await db.commit()
    return {"message": f"Subject {subject.name} removed from group {group.name}"}

@group_subject_router.delete("/group/{group_id}/subjects")
async def clear_group_subjects(
    group_id: int,
    db: AsyncSession = Depends(get_db)
):
    # Fetch the group
    group = await db.get(Group, group_id)
    if not group:
        return {"error": "Group not found"}

    # Clear all subjects
    group.subjects = []

    # Commit the changes
    await db.commit()
    return {"message": f"All subjects removed from group {group.name}"}

