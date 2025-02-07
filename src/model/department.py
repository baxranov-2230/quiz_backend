from sqlalchemy import Column , Integer , String , ForeignKey
from sqlalchemy.orm import relationship
from src.settings.base import Base

class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculties.id"), nullable=False)
    
    faculty = relationship("Faculty", back_populates="departments")
    teachers = relationship("Teacher", back_populates="department", cascade="all, delete")