from sqlalchemy import Column , Integer , String , ForeignKey
from sqlalchemy.orm import relationship
from src.settings.base import Base
from src.model.teacher_group_association import teacher_group_association
from src.model.group_subject_association import group_subject_association


class Group(Base):
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(25), nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculties.id"), nullable=False)
    


    students = relationship("Student", back_populates="group", cascade="all, delete")
    faculties = relationship("Faculty", back_populates="groups")
    user_tests = relationship("UserTest", back_populates="group")
    
    teachers = relationship("Teacher", secondary=teacher_group_association, back_populates="groups")
    subjects = relationship("Subject", secondary=group_subject_association, back_populates="groups")
