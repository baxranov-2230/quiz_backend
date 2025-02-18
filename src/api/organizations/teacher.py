from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.base import get_db
from src.CRUD.CRUDBase import CRUDBaseAsync
from src.model import Teacher , User
from sqlalchemy import select   
from src.auth.utils import get_current_user
from src.schemas import TeacherUpdate

teacher_router = APIRouter(
    tags=['Teacher']
)

main_crud = CRUDBaseAsync(Teacher)


@teacher_router.get("/teacher-get/{id}")
async def teacher_get_id(teacher_id: int , db: AsyncSession = Depends(get_db)):
    return main_crud.get(db , id = teacher_id)

@teacher_router.get("/teacher-get-all")
async def teacher_get_all(db : AsyncSession = Depends(get_db)):
    return main_crud.get_all(db)

@teacher_router.put("/teacher-update/{id}")
async def teacher_update(id: int , teacher_in: TeacherUpdate, db : AsyncSession = Depends(get_db)):
    return await main_crud.update(db , id , obj_in=teacher_in)

@teacher_router.delete("/teacher-delete/{id}")
async def teacher_delete(
    id: int , 
    user_info: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)):
    current_user = await db.execute(select(Teacher).where(Teacher.user_id == user_info.id))
    user = current_user.scalars.first()
    
    await db.delete(user)
    await main_crud.delete(db, id)
    await db.commit()
    
    return {"message": "Teacher deleted successfully"}
    
    