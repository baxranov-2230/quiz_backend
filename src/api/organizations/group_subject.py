from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.base import get_db
from src.CRUD.CRUDBase import CRUDBaseAsync
from src.model.group_subject_association import group_subject_association
from src.schemas.group_subject_association import (
    GroupSubjectAssociationCreate,
    GroupSubjectAssociationUpdate,
)

group_subject_association_router = APIRouter(
    tags=["Group Subject Association"]
)

main_crud = CRUDBaseAsync(group_subject_association)

@group_subject_association_router.post("/create_group_subject_association")
async def create_group_subject_association(
    group_subject_association: GroupSubjectAssociationCreate,
    db: AsyncSession = Depends(get_db)    
):
    return await main_crud.create(db, obj_in=group_subject_association)

@group_subject_association_router.get("/group_subject_association_get_all")
async def get_group_subject_associations(
    db: AsyncSession = Depends(get_db)
):
    return await main_crud.get_all(db)

@group_subject_association_router.get("/group_subject_association_get/{association_id}")
async def get_group_subject_association_by_id(
    association_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await main_crud.get(db, id=association_id)

@group_subject_association_router.put("/group_subject_association_update/{association_id}")
async def update_group_subject_association(
    association_id: int,
    association_in: GroupSubjectAssociationUpdate,
    db: AsyncSession = Depends(get_db)
):
    return await main_crud.update(db, id=association_id, obj_in=association_in)

@group_subject_association_router.delete("/group_subject_association_delete/{association_id}")
async def delete_group_subject_association(
    association_id: int,
    db: AsyncSession = Depends(get_db)
):
    await main_crud.delete(db, id=association_id)
    return {"message": "Group subject association deleted successfully"}
