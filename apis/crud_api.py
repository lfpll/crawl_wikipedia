from fastapi import FastAPI,Depends,HTTPException
from models  import Url,UrlBase
from pydantic import HttpUrl

from db import SessionLocal,BaseDbModel,engine
from sqlalchemy.orm import Session
import crud 

app = FastAPI()

BaseDbModel.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Read
@app.get("/url/{url}",response_model=Url)
def get_url_information(url:HttpUrl,db:Session = Depends(get_db)):
    url_info = crud.get_url(db=db,url=url)
    if not url_info:
        raise HTTPException(status_code=404, detail="Url doens't exist")
    return url_info

# Insert
@app.post("/url/",response_model=UrlBase)
def create_url_endpoint(url:UrlBase,db:Session = Depends(get_db)):
    url_info = crud.get_url(db=db,url=url)
    if url_info:
        raise HTTPException(status_code=400, detail="Url already exist")
    return crud.create_url(db=db,url=url)

    
# Update
@app.put("/url/{url}",response_model=UrlBase)
def update_url_endpoint(url:HttpUrl,update_data:UrlBase,db:Session = Depends(get_db)):
    url_info = crud.get_url(db=db,url=url)
    if not url_info:
        raise HTTPException(status_code=404, detail="Url doens't exist")
    return crud.update_url(db=db,url=url,data=update_data)


@app.put("/url/increment/{url}",response_model=UrlBase)
def increment_url(url:HttpUrl, db: Session = Depends(get_db)):
    url_info = get_url_information(url=url,db=db)
    return crud.increment_url(url=url,db=db)