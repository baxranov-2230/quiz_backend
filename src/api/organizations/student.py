from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.base import get_db
from src.CRUD.CRUDBase import CRUDBaseAsync
from src.model import Student , User
from sqlalchemy import select   
from src.auth.utils import get_current_user
from src.schemas import StudentUpdate

student_router = APIRouter(
    tags=['Student']
)

main_crud = CRUDBaseAsync(Student)


@student_router.get("/student-get/{student_id}")
async def student_get_id(student_id: int , db: AsyncSession = Depends(get_db)):
    return main_crud.get(db , id = student_id)

@student_router.get("/student-get-all")
async def student_get_all(db : AsyncSession = Depends(get_db)):
    return main_crud.get_all(db)

@student_router.put("/student-update/{student_id}")
async def student_update(student_id: int , student_in: StudentUpdate, db : AsyncSession = Depends(get_db)):
    return main_crud.update(db , id = student_id, obj_in=student_in)

@student_router.delete("/student-delete/{id}")
async def student_delete(
    student_id : int , 
    user_info: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):
    current_user = await db.execute(select(Student).where(Student.user_id == user_info.id))
    user = current_user.scalars.first()
    
    await db.delete(user)
    await main_crud.delete(db, id = student_id)
    await db.commit()
    
    return {"message": "Student deleted successfully"}
    
    