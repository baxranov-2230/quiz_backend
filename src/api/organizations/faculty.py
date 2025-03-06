from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.base import get_db
from src.CRUD.CRUDBase import CRUDBaseAsync
from src.model import Faculty 
from src.schemas import FacultyCreate , FacultyUpdate


faculty_router = APIRouter(
    tags=["Faculty"]
)

main_crud = CRUDBaseAsync(Faculty)

@faculty_router.post("/faculty-create")
async def faculty(faculty: FacultyCreate, db : AsyncSession = Depends(get_db)):
    return await main_crud.create(db, obj_in=faculty)



@faculty_router.get("/faculty-get/{faculty_id}")
async def faculty_get_id(faculty_id: int, db: AsyncSession = Depends(get_db)):
    return await main_crud.get(db , id = faculty_id)

@faculty_router.get("/faculty-get-all")
async def faculty_get_all(db : AsyncSession = Depends(get_db)):
    return await main_crud.get_all(db)

@faculty_router.put("/faculty-update/{faculty_id}")
async def faculty_update(
    faculty_id: int, 
    faculty_in : FacultyUpdate , 
    db : AsyncSession = Depends(get_db)):
    return await main_crud.update(db, id = faculty_id, obj_in=faculty_in)

@faculty_router.delete("/faculty-delete/{faculty_id}")
async def faculty_delete(
    faculty_id: int, 
    db: AsyncSession = Depends(get_db)):
    await main_crud.delete(db , id = faculty_id)
    return {"message": "Faculty deleted successfully"}


