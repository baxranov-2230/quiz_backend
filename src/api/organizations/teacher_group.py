from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.base import get_db
from src.CRUD.CRUDBase import CRUDBaseAsync
from src.model.teacher_group_association import teacher_group_association
from src.schemas.teacher_group_association import TeacherGroupAssociationCreate, TeacherGroupAssociationUpdate

teacher_group_router = APIRouter(
    tags=["Teacher Group Association"]
)

main_crud = CRUDBaseAsync(teacher_group_association)

@teacher_group_router.post("/create_teacher_group_association")
async def create_teacher_group_association(
    teacher_group_association: TeacherGroupAssociationCreate,
    db: AsyncSession = Depends(get_db)    
):
    return await main_crud.create(db, obj_in=teacher_group_association)

@teacher_group_router.get("/teacher_group_association_get_all")
async def get_teacher_group_associations(
    db: AsyncSession = Depends(get_db)
):
    return await main_crud.get_all(db)

@teacher_group_router.get("/teacher_group_association_get/{teacher_group_association_id}")
async def get_teacher_group_association_by_id(
    teacher_group_association_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await main_crud.get(db, id=teacher_group_association_id)

@teacher_group_router.put("/teacher_group_association_update/{teacher_group_association_id}")
async def update_teacher_group_association(
    teacher_group_association_id: int,
    teacher_group_association_in: TeacherGroupAssociationUpdate,
    db: AsyncSession = Depends(get_db)
):
    return await main_crud.update(db, id=teacher_group_association_id, obj_in=teacher_group_association_in)

@teacher_group_router.delete("/teacher_group_association_delete/{teacher_group_association_id}")
async def delete_teacher_group_association(
    teacher_group_association_id: int,
    db: AsyncSession = Depends(get_db)
):
    await main_crud.delete(db, id=teacher_group_association_id)
    return {"message": "Teacher group association deleted successfully"}
