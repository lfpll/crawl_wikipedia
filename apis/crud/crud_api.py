from fastapi import FastAPI,Depends,HTTPException
from apis.crud.schemas  import UrlBase,Url
from apis.crud.db import SessionLocal,BaseDbModel,engine
from apis.crud import crud
from pydantic import HttpUrl

from sqlalchemy.orm import Session


app = FastAPI()

BaseDbModel.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Read
@app.get("/url/{url:path}",response_model=Url)
async def get_url_information(url:HttpUrl,db:Session = Depends(get_db)):
    url_info = crud.get_url(db=db,url=url)
    if not url_info:
        raise HTTPException(status_code=404, detail="Url doens't exist")
    return url_info

# Insert
@app.post("/url/",response_model=Url)
async def create_url_endpoint(url:Url,db:Session = Depends(get_db)):
    url_info = crud.get_url(db=db,url=url.url)
    if url_info:
        raise HTTPException(status_code=400, detail="Url already exist")
    new_url = crud.create_url(db=db,url=url) 
    return new_url

@app.put("/url/increment/{url:path}")
def increment_url(url: HttpUrl, db: Session = Depends(get_db)):
    url_info = crud.get_url(url=url,db=db)
    if url_info:
        data = crud.increment_url(url=url,db=db)
        return data
    else:
        return crud.create_url(url=Url(url=url),db=db)
        
    
# Update
@app.put("/url/{url:path}",response_model=Url)
async def update_url_endpoint(url:HttpUrl,update_data:UrlBase,db:Session = Depends(get_db)):
    url_info = crud.get_url(db=db,url=url)
    if not url_info:
        raise HTTPException(status_code=404, detail="Url doens't exist")
    return crud.update_url(db=db,url=url,data=update_data)


