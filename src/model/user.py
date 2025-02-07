from sqlalchemy import Column , String , Boolean, Integer, Enum
from sqlalchemy.orm import relationship
from src.settings.base import Base
import enum

class UserRole(enum.Enum):
    student = "student"
    teacher = "teacher"
    admin = "admin"



class User(Base):
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole))
    disabled = Column(Boolean)
    
    student = relationship("Student", back_populates="user", uselist=False)
    teacher = relationship("Teacher", back_populates="user", uselist=False)