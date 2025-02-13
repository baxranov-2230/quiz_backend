from sqlalchemy import Column , Integer , String , ForeignKey
from sqlalchemy.orm import relationship
from src.settings.base import Base
from model.teacherandgroup import teacher_group_association


class Group(Base):
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(25), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    

    subjects = relationship("Subject", back_populates="group", cascade="all, delete")
    students = relationship("Student", back_populates="group", cascade="all, delete")
    department = relationship("Department", back_populates="groups")
    
    