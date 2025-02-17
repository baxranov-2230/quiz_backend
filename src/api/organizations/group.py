from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.base import get_db
from src.CRUD.CRUDBase import CRUDBaseAsync
from src.model import Group
from src.schemas import GroupUpdate , GroupCreate

group_router = APIRouter()

main_crud = CRUDBaseAsync(Group)

@group_router.post("/group-create")
async def add_group(
    group: GroupCreate,
    db: AsyncSession = Depends(get_db)):
    return await main_crud.create(db, obj_in=group)

@group_router.get("/group-get-all")
async def get_group(db: AsyncSession = Depends(get_db)):
    return await main_crud.get_all(db)

@group_router.get("/group-get/{id}")
async def get_group_by_id(id: int, db: AsyncSession = Depends(get_db)):
    return await main_crud.get(db, id)

@group_router.put("/group-update/{id}")
async def update_group(
    id: int, 
    group_in : GroupUpdate,
    db: AsyncSession = Depends(get_db)):
    await main_crud.update(db , id , obj_in=group_in)
    return await main_crud.update(db, id)

@group_router.delete("/group-delete/{id}")
async def delete_group(db : AsyncSession = Depends(get_db)):
    await main_crud.delete(db, id)
    return {"message": "Group deleted successfully"}