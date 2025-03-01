from sqlalchemy import Column , Integer , String , ForeignKey
from sqlalchemy.orm import relationship
from src.settings.base import Base
from src.model.teacher_group_association import teacher_group_association

class Teacher(Base):
    __tablename__ = "teachers"
    
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    last_name = Column(String(50), nullable=True)
    first_name = Column(String(50), nullable=True)
    patronymic = Column(String(50), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    jshir = Column(String(14), unique=True, nullable=True)
    passport = Column(String(20), unique=True, nullable=True)
    
    department = relationship("Department", back_populates="teachers")
    user = relationship("User", back_populates="teacher", uselist=False)
    subjects = relationship("Subject", back_populates="teacher", cascade="all, delete")
    questions = relationship("Question", back_populates="teacher", cascade="all, delete-orphan")
    
    groups = relationship("Group", secondary=teacher_group_association, back_populates="teachers")
    user_tests = relationship("UserTest", back_populates="teacher")
