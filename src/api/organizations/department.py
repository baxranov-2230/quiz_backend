from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.base import get_db
from src.CRUD.CRUDBase import CRUDBaseAsync
from src.model import Department , Faculty
from src.schemas import DepartmentUpdate, DepartmentCreate
from sqlalchemy import select

department_router = APIRouter()

main_crud = CRUDBaseAsync(Department)


@department_router.post("/department-create")
async def department(department: DepartmentCreate, db : AsyncSession = Depends(get_db)):
    some_id = await db.execute(select(Faculty).where(Faculty.id == department.faculty_id))
    result = some_id.scalars().first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found faculty"
        )
    return await main_crud.create(db, obj_in=department)


@department_router.get("/department-get/{id}")
async def department_get_id(department_id: int, db: AsyncSession = Depends(get_db)):
    return await main_crud.get(db , id = department_id)

@department_router.get("/department-get-all")
async def department_get_all(db : AsyncSession = Depends(get_db)):
    return await main_crud.get_all(db)

@department_router.put("/department-update/{id}")
async def department_update(
    department_id: int, 
    department_in : DepartmentUpdate , 
    db : AsyncSession = Depends(get_db)):
    return await main_crud.update(db, id = department_id, obj_in=department_in)

@department_router.delete("/department-delete/{id}")
async def department_delete(
    department_id: int,
    db: AsyncSession = Depends(get_db)):
    await main_crud.delete(db, id = department_id)
    
    return {"message": "Department deleted successfully"}