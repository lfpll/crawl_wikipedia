# File with pydantic and db models
from sqlalchemy import String,Integer,Column,Float,Boolean
from apis.crud.db import BaseDbModel

# DB model
class UrlDbModel(BaseDbModel):
    __tablename__ = "urls"
    
    # Asserting some rules to garantee data quality
    id = Column(Integer,primary_key=True, index=True)
    url = Column(String,unique=True,index=True,nullable=False)
    appearances = Column(Integer,nullable=False,default=1)
    is_file =  Column(Boolean,nullable=True)
    percent_of_letters_path =  Column(Float,nullable=True)
    percent_of_numbers_path =  Column(Float,nullable=True)
    path_length =  Column(Integer,nullable=True)
    last_path_length =  Column(Integer,nullable=True)
    full_lengh =  Column(Integer,nullable=True)
    is_arabic =  Column(Boolean,nullable=True)
    number_of_subpaths =  Column(Integer,nullable=True)
    related_original_url = Column(Boolean,nullable=True)
    domain_length        = Column(Integer,nullable=True)
