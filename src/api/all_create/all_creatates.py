from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.base import get_db
from src.CRUD.CRUDBase import CRUDBaseAsync
from src.model import Faculty , Department, Group
from src.schemas import FacultyCreate


post_router = APIRouter()

main_crud = CRUDBaseAsync(Faculty , Department, Group)

@post_router.post("/faculty-create")
async def faculty(faculty: FacultyCreate, db : AsyncSession = Depends(get_db)):
    return await main_crud.create(db, obj_in=faculty.name)



@post_router.get("/faculty-get/{id}")
async def faculty_get_id(id: int, db: AsyncSession = Depends(get_db)):
    return await main_crud.get(db , id = id)

@post_router.get("/faculty-get-all")
async def faculty_get_all(db : AsyncSession = Depends(get_db)):
    return await main_crud.get_all(db)