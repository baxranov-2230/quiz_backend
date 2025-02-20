from pydantic import BaseModel, HttpUrl
from typing import Optional

    
class QuestionBase(BaseModel):
    text: Optional[str] = None
    image: Optional[HttpUrl] = None  # URL for question image
    option_a: Optional[str] = None
    option_a_image: Optional[HttpUrl] = None  # URL for option A image
    option_b: Optional[str] = None
    option_b_image: Optional[HttpUrl] = None  # URL for option B image
    option_c: Optional[str] = None
    option_c_image: Optional[HttpUrl] = None  # URL for option C image
    option_d: Optional[str] = None
    option_d_image: Optional[HttpUrl] = None 
    
class QuestionText(BaseModel):
    text: Optional[str] = None
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None

class QuestionImage(BaseModel):
    option_a_image: Optional[HttpUrl] = None 
    option_b_image: Optional[HttpUrl] = None
    option_c_image: Optional[HttpUrl] = None
    option_d_image: Optional[HttpUrl] = None 


class QuestionUpdate(BaseModel):
    text: Optional[str] = None
    image: Optional[HttpUrl] = None  # URL for question image
    option_a: Optional[str] = None
    option_a_image: Optional[HttpUrl] = None  # URL for option A image
    option_b: Optional[str] = None
    option_b_image: Optional[HttpUrl] = None  # URL for option B image
    option_c: Optional[str] = None
    option_c_image: Optional[HttpUrl] = None  # URL for option C image
    option_d: Optional[str] = None
    option_d_image: Optional[HttpUrl] = None 
    
class QuestionResponse(QuestionBase):
    id : int
    
    class Config:
        from_attributes = True