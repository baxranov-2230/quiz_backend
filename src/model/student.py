from sqlalchemy import Column , Integer , String , ForeignKey
from sqlalchemy.orm import relationship
from src.settings.base import Base

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    jshir = Column(String(15), unique=True, nullable=False)
    passport = Column(String(20), unique=True, nullable=False)
    
    group = relationship("Group", back_populates="students")
    results = relationship("ResultStudent", back_populates="student", cascade="all, delete")
    user = relationship("User", back_populates="student", uselist=False)