from sqlalchemy import Column , Integer , String
from sqlalchemy.orm import relationship
from src.settings.base import Base

class Faculty(Base):
    __tablename__ = "faculties"
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    
    departments = relationship("Department", back_populates="faculty", cascade="all, delete")
    groups = relationship("Group", back_populates="faculties", cascade="all, delete")