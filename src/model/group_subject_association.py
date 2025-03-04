from sqlalchemy import Table, Column, Integer, ForeignKey
from src.settings.base import Base

group_subject_association = Table(
    "group_subject_association",
    Base.metadata,
    Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True),
    Column("subject_id", Integer, ForeignKey("subjects.id"), primary_key=True),
)
