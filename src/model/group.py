from sqlalchemy import Column , Integer , String , ForeignKey
from sqlalchemy.orm import relationship
from src.settings.base import Base


class Group(Base):
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(25), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    
    teacher = relationship("Teacher", back_populates="groups")
    subjects = relationship("Subject", back_populates="group", cascade="all, delete")
    students = relationship("Student", back_populates="group", cascade="all, delete")