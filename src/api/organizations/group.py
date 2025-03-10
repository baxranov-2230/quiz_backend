from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.base import get_db
from src.CRUD.CRUDBase import CRUDBaseAsync
from src.model import Group, Faculty
from src.schemas import GroupUpdate , GroupCreateRequest
from sqlalchemy.future import select

group_router = APIRouter(
    tags=["Group"]
)

main_crud = CRUDBaseAsync(Group)

@group_router.post("/group-create")
async def add_group(
    group: GroupCreateRequest,
    db: AsyncSession = Depends(get_db)):
    
    new_group = await main_crud.create(db, obj_in=group)
    
    stmt = select(Faculty).where(Faculty.id == new_group.faculty_id)
    result = await db.execute(stmt)
    faculty = result.scalars().first()  # Extract the actual faculty object

    if not faculty:
        raise HTTPException(status_code=404, detail="Faculty not found")

    return {
        "id": new_group.id,
        "name": new_group.name,
        "faculty": faculty.name,
        "faculty_id": faculty.id
    }

@group_router.get("/group-get-all")
async def get_group(db: AsyncSession = Depends(get_db)):
    return await main_crud.get_all(db)

@group_router.get("/group-get/{group_id}")
async def get_group_by_id(group_id: int, db: AsyncSession = Depends(get_db)):
    return await main_crud.get(db, id = group_id)

@group_router.put("/group-update/{group_id}")
async def update_group(
    group_id: int, 
    group_in : GroupUpdate,
    db: AsyncSession = Depends(get_db)):
    return await main_crud.update(db , id = group_id , obj_in=group_in)

@group_router.delete("/group-delete/{group_id}")
async def delete_group(
    group_id: int,
    db : AsyncSession = Depends(get_db)):
    await main_crud.delete(db, id = group_id)
    return {"message": "Group deleted successfully"}