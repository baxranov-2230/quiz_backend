from sqlalchemy import Column , Integer , ForeignKey 
from sqlalchemy.orm import relationship
from src.settings.base import Base

class TeacherAndGroup(Base):
    __tablename__ = "teacher_and_group"
    
    teacher_id = Column(Integer, ForeignKey("teachers.id"), primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.id"), primary_key=True) 




    teacher = relationship("Teacher", back_populates="groups")
    group = relationship("Group", back_populates="teachers")
    