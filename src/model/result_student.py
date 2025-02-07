from sqlalchemy import Column , Integer, ForeignKey, DateTime, JSON, func
from sqlalchemy.orm import relationship
from src.settings.base import Base



class ResultStudent(Base):
    __tablename__ = "result_students"
    
    id = Column(Integer, primary_key=True, nullable=False)
    grade = Column(Integer, nullable=False)
    result_time = Column(DateTime, default=func.now())
    quiz = Column(JSON, nullable=False)
    
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    
    student = relationship("Student", back_populates="results")
    subject = relationship("Subject", back_populates="results")
    