from sqlalchemy import Column , Integer , String , ForeignKey
from sqlalchemy.orm import relationship
from src.settings.base import Base

class Teacher(Base):
    __tablename__ = "teachers"
    
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    jshir = Column(String(14), unique=True, nullable=False)
    
    department = relationship("Department", back_populates="teachers")
    subjects = relationship("Subject", back_populates="teacher", cascade="all, delete")
    groups = relationship("Group", back_populates="teacher", cascade="all, delete")
    user = relationship("User", back_populates="teacher", uselist=False)
    
    

    
    