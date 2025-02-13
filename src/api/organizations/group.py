from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.base import get_db
from src.CRUD.CRUDBase import CRUDBaseAsync
from src.model import Group
from src.schemas import DepartmentUpdate, DepartmentCreate

group_router = APIRouter()

main_crud = CRUDBaseAsync(Group)

