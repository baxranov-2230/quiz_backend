from pydantic import BaseModel, HttpUrl
from typing import Optional


class QuestionBase(BaseModel):
    text: Optional[str] = None
    image: Optional[HttpUrl] = None
    option_a: Optional[str] = None
    option_a_image: Optional[HttpUrl] = None  
    option_b: Optional[str] = None
    option_b_image: Optional[HttpUrl] = None  
    option_c: Optional[str] = None
    option_c_image: Optional[HttpUrl] = None  
    option_d: Optional[str] = None
    option_d_image: Optional[HttpUrl] = None 

    class Config:
        from_attributes = True


class QuestionCreateRequest(QuestionBase):
    class Config:
        from_attributes = True


class QuestionCreateResponse(QuestionBase):
    id: int

    class Config:
        from_attributes = True


class QuestionText(BaseModel):
    text: Optional[str] = None
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None

    class Config:
        from_attributes = True

class QuestionImage(BaseModel):
    option_a_image: Optional[HttpUrl] = None 
    option_b_image: Optional[HttpUrl] = None
    option_c_image: Optional[HttpUrl] = None
    option_d_image: Optional[HttpUrl] = None 

    class Config:
        from_attributes = True

class QuestionUpdate(BaseModel):
    text: Optional[str] = None
    image: Optional[HttpUrl] = None
    option_a: Optional[str] = None
    option_a_image: Optional[HttpUrl] = None  
    option_b: Optional[str] = None
    option_b_image: Optional[HttpUrl] = None  
    option_c: Optional[str] = None
    option_c_image: Optional[HttpUrl] = None  
    option_d: Optional[str] = None
    option_d_image: Optional[HttpUrl] = None 

    class Config:
        from_attributes = True


class QuestionResponse(QuestionBase):
    id: int
    
    class Config:
        from_attributes = True