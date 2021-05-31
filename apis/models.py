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
    appearances = Column(Integer,nullable=True,default=1)
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
    url : str

class Url(UrlBase):
    id: int
    appearances: Optional[int] = 1
    f0:  Optional[str] = None
    f1:  Optional[str] = None
    f2:  Optional[str] = None
    f3:  Optional[str] = None
    f4:  Optional[str] = None
    f5:  Optional[str] = None
    f6:  Optional[str] = None
    f7:  Optional[str] = None
    f8:  Optional[str] = None
    f9:  Optional[str] = None
    f10: Optional[str] = None
