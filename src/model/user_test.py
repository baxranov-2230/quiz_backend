from sqlalchemy import Column , String , Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.settings.base import Base

class UserTest(Base):
    __tablename__ = "user_tests"
    
    id = Column(Integer, primary_key=True, nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    
    teacher = relationship("Teacher", back_populates="user_tests")
    subject = relationship("Subject", back_populates="user_tests")
    group = relationship("Group", back_populates="user_tests")
    