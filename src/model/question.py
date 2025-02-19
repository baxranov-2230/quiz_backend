from sqlalchemy import Column , Integer , String , Text, ForeignKey
from sqlalchemy.orm import relationship
from src.settings.base import Base

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=True)
    image = Column(String, nullable=True)
    option_a = Column(String, nullable=True)
    option_a_image = Column(String, nullable=True)
    option_b = Column(String, nullable=True)
    option_b_image = Column(String, nullable=True)
    option_c = Column(String, nullable=True)
    option_c_image = Column(String, nullable=True)
    option_d = Column(String, nullable=True)
    option_d_image = Column(String, nullable=True)
    
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    subject_id = Column(Integer , ForeignKey("subjects.id"))
    
    teacher = relationship("Teacher", back_populates="questions")
    subject = relationship("Subject", back_populates="questions") 
    

    