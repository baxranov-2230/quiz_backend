from sqlalchemy import Table, Column, Integer, ForeignKey
from src.settings.base import Base

teacher_group_association = Table(
    "teacher_group_association",
    Base.metadata,
    Column("teacher_id", Integer, ForeignKey("teachers.id"), primary_key=True),
    Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True)
)