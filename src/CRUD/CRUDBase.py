from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert 
from typing import Type, TypeVar, Generic, List , Optional
from src.model import Faculty 
from fastapi import HTTPException
from src.settings.base import Base

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType")

class CRUDBaseAsync(Generic[ModelType, SchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> ModelType:
        result = await db.execute(select(self.model).filter(self.model.id == id))
        db_obj = result.scalars().first()
        if not db_obj:
            raise HTTPException(status_code=404, detail="Item not found")
        return db_obj

    async def get_all(self, db: AsyncSession, limit: Optional[int] = 100) -> List[ModelType]:
        result = await db.execute(select(self.model).limit(limit))
        return result.scalars().all()

    async def get_all_name(self , db : AsyncSession, limit: Optional[int] = 100):
        stmt = (
            select(
                self.model.name, 
                self.model.id,
                Faculty.name.label("faculty")
                )
            .join(Faculty, self.model.faculty_id == Faculty.id)
            .limit(limit)
        )
        result = await db.execute(stmt)
        rows = result.mappings().all()
        return rows


    async def create(self, db: AsyncSession, obj_in: SchemaType) -> ModelType:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, id: int, obj_in: SchemaType) -> ModelType:
        db_obj = await self.get(db, id)
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, id: int) -> None:
        db_obj = await self.get(db, id)
        await db.delete(db_obj)
        await db.commit()
        
    async def insert_many_to_many(self, db: AsyncSession, obj_in: SchemaType):
        stmt = insert(self.model).values(**obj_in.model_dump())  
        await db.execute(stmt)
        await db.commit()
        return {"message": "Association created successfully"}
