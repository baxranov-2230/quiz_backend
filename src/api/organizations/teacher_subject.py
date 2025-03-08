from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.base import get_db
from src.CRUD.CRUDBase import CRUDBaseAsync
from src.model.teacher_subject_association import teacher_subject_association
from src.schemas.teacher_subject_association import TeacherSubjectAssociationCreate, TeacherSubjectAssociationUpdate

teacher_subject_router = APIRouter(
    tags=["Teacher Subject Association"]
)

main_crud = CRUDBaseAsync(teacher_subject_association)

@teacher_subject_router.post("/create_teacher_subject_association")
async def create_teacher_subject_association(
    teacher_subject_association: TeacherSubjectAssociationCreate,
    db: AsyncSession = Depends(get_db)    
):
    return await main_crud.create(db, obj_in=teacher_subject_association)

@teacher_subject_router.get("/teacher_subject_association_get_all")
async def get_teacher_subject_associations(
    db: AsyncSession = Depends(get_db)
):
    return await main_crud.get_all(db)

@teacher_subject_router.get("/teacher_subject_association_get/{teacher_subject_association_id}")
async def get_teacher_subject_association_by_id(
    teacher_subject_association_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await main_crud.get(db, id=teacher_subject_association_id)

@teacher_subject_router.put("/teacher_subject_association_update/{teacher_subject_association_id}")
async def update_teacher_subject_association(
    teacher_subject_association_id: int,
    teacher_subject_association_in: TeacherSubjectAssociationUpdate,
    db: AsyncSession = Depends(get_db)
):
    return await main_crud.update(db, id=teacher_subject_association_id, obj_in=teacher_subject_association_in)

@teacher_subject_router.delete("/teacher_subject_association_delete/{teacher_subject_association_id}")
async def delete_teacher_subject_association(
    teacher_subject_association_id: int,
    db: AsyncSession = Depends(get_db)
):
    await main_crud.delete(db, id=teacher_subject_association_id)
    return {"message": "Teacher subject association deleted successfully"}
