from sqlalchemy import Column , Integer , String , ForeignKey
from sqlalchemy.orm import relationship
from src.model.teacher_subject_association import teacher_subject_association
from src.model.group_subject_association import group_subject_association

from src.settings.base import Base

class Subject(Base):
    __tablename__ = "subjects"
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id") ,nullable=True)

    groups = relationship("Group", back_populates="subjects") 
    user_tests = relationship("UserTest", back_populates="subject")
    results = relationship("ResultStudent", back_populates="subject", cascade="all, delete")
    questions = relationship("Question", back_populates="subject", cascade="all, delete-orphan")
    department = relationship("Department", back_populates="subjects")
    


    teachers = relationship("Teacher", secondary=teacher_subject_association, back_populates="subjects")
    groups = relationship("Group", secondary=group_subject_association, back_populates="subjects")