from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.settings.base import Base

teacher_subject_association = Table(
    "teacher_subject_association",
    Base.metadata,
    Column("teacher_id", Integer, ForeignKey("teachers.id"), primary_key=True),
    Column("subject_id", Integer, ForeignKey("subjects.id"), primary_key=True),
)