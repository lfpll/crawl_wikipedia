# File with pydantic and db models
from sqlalchemy import String,Integer,Column
from db import BaseDbModel
from pydantic import BaseModel,HttpUrl
from pydantic.typing import Optional


# DB model
class UrlDbModel(BaseDbModel):
    __tablename__ = "urls"
    
    # Asserting some rules to garantee data quality
    id = Column(Integer,primary_key=True, index=True)
    url = Column(String,unique=True,index=True,nullable=False)
    appearances = Column(Integer,index=True,nullable=True)
    f0 =  Column(String,nullable=True)  
    f1 =  Column(String,nullable=True)
    f2 =  Column(String,nullable=True)
    f3 =  Column(String,nullable=True)
    f4 =  Column(String,nullable=True)
    f5 =  Column(String,nullable=True)
    f6 =  Column(String,nullable=True)
    f7 =  Column(String,nullable=True)
    f8 =  Column(String,nullable=True)
    f9 =  Column(String,nullable=True)
    f10 = Column(String,nullable=True)

# Pydantic Models
class UrlBase(BaseModel):
    url : HttpUrl

class Url(UrlBase):
    appearances: Optional[int]
    f0:  Optional[str]
    f1:  Optional[str]
    f2:  Optional[str]
    f3:  Optional[str]
    f4:  Optional[str]
    f5:  Optional[str]
    f6:  Optional[str]
    f7:  Optional[str]
    f8:  Optional[str]
    f9:  Optional[str]
    f10: Optional[str]
