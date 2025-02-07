from sqlalchemy import Column , Integer , String , ForeignKey
from sqlalchemy.orm import relationship
from src.settings.base import Base

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    last_name = Column(String(50), nullable=True)
    first_name = Column(String(50), nullable=True)
    patronymic = Column(String(50), nullable=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    jshir = Column(String(15), unique=True, nullable=True)
    passport = Column(String(20), unique=True, nullable=True)
    
    group = relationship("Group", back_populates="students")
    results = relationship("ResultStudent", back_populates="student", cascade="all, delete")
    user = relationship("User", back_populates="student", uselist=False)