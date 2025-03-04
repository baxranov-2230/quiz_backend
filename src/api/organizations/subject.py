from fastapi import APIRouter , Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.base import get_db
from src.CRUD.CRUDBase import CRUDBaseAsync
from src.schemas.subject import SubjectCreateRequest, SubjectUpdate
from src.model.subject import Subject

subject_router = APIRouter(
    tags=["Subject"]
)


main_crud = CRUDBaseAsync(Subject)

@subject_router.post("/create-subject")
async def create_subject(
    subject_item: SubjectCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    return  await main_crud.create(db , obj_in=subject_item)

@subject_router.get("/subject-get-all")
async def get_all(
    db: AsyncSession = Depends(get_db)
):
    return await main_crud.get_all(db)

@subject_router.get("/subject-get/{subject_id}")
async def get_by_id(
    subject_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await main_crud.get(db , id = subject_id)

@subject_router.put("/subject-update/{subject_id}")
async def update_group(
    subject_id : int,
    subject_in: SubjectUpdate,
    db: AsyncSession = Depends(get_db)
):
    return await main_crud.update(db , id=subject_id , obj_in=subject_in)

@subject_router.delete("/subject-delete/{subject_id}")
async def delete_subject(
    subject_id: int,
    db : AsyncSession = Depends(get_db)

):  
    await main_crud.delete(db , id=subject_id)
    return {"message": "Subject deleted successfully"}