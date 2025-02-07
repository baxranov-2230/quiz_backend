from sqlalchemy import Column , Integer , String , Text, ForeignKey
from src.settings.base import Base

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer , primary_key=True , nullable=False)
    text = Column(Text , nullable=False)
    imgae = Column(String , nullable=True)
    A = Column(String , nullable=False)
    B = Column(String , nullable=False)
    C = Column(String , nullable=False)
    D = Column(String , nullable=False)
    
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    subject_id = Column(Integer , ForeignKey("subkects.id"))
    
    