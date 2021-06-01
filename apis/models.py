# File with pydantic and db models
from sqlalchemy import String,Integer,Column,Float,Boolean
from db import BaseDbModel
from pydantic import BaseModel,HttpUrl
from pydantic.typing import Optional,Set



# DB model
class UrlDbModel(BaseDbModel):
    __tablename__ = "urls"
    
    # Asserting some rules to garantee data quality
    id = Column(Integer,primary_key=True, index=True)
    url = Column(String,unique=True,index=True,nullable=False)
    appearances = Column(Integer,nullable=False,default=1)
    domain =  Column(String,nullable=True)  
    path =  Column(String,nullable=True)
    is_file =  Column(Boolean,nullable=True)
    percent_of_letters_path =  Column(Float,nullable=True)
    percent_of_numbers_path =  Column(Float,nullable=True)
    path_length =  Column(Integer,nullable=True)
    last_path_length =  Column(Integer,nullable=True)
    full_lengh =  Column(Integer,nullable=True)
    is_arabic =  Column(Boolean,nullable=True)
    number_of_subpaths =  Column(Integer,nullable=True)
    related_original_url = Column(Boolean,nullable=True)

# Pydantic Models
class UrlBase(BaseModel):
    id: int
    url : str

    class Config:
        orm_mode = True


class Url(UrlBase):
    appearances: Optional[int]
    domain:  Optional[str]
    path:  Optional[str]
    is_file:  Optional[bool]
    is_arabic:  Optional[bool]
    last_path_length:  Optional[int]
    percent_of_letters_path:  Optional[float]
    percent_of_numbers_path:  Optional[float]
    path_length:  Optional[int]
    full_lengh:  Optional[int]
    number_of_subpaths:  Optional[int]
    related_original_url: Optional[bool]

