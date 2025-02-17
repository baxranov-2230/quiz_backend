from sqlalchemy import Column , Integer , String , ForeignKey
from sqlalchemy.orm import relationship
from src.settings.base import Base

class Subject(Base):
    __tablename__ = "subjects"
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    
    teacher = relationship("Teacher", back_populates="subjects")
    group = relationship("Group", back_populates="subjects")
    results = relationship("ResultStudent", back_populates="subject", cascade="all, delete")
    questions = relationship("Question", back_populates="subject", cascade="all, delete-orphan")
    
    user_tests = relationship("UserTest", back_populates="subject")