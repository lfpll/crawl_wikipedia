from models import UrlBase,UrlDbModel,Url
from pydantic import HttpUrl
from sqlalchemy.orm import Session
from sqlalchemy import update


def create_url(db: Session,url:UrlBase):
    new_url = UrlDbModel(url=url)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url

def get_url(db:Session, url:UrlBase):
    return db.query(UrlDbModel.url == url).limit(1).all()

def update_url(db:Session,url:HttpUrl,data:Url) -> Url:
    data = db.query().where(UrlDbModel.url == url).update(
        appearances = data.appearances,
        f0 = data.f0,
        f1 = data.f1,
        f2 = data.f2,
        f3 = data.f3,
        f4 = data.f4,
        f5 = data.f5,
        f6 = data.f6,
        f7 = data.f7,
        f8 = data.f8,
        f9 = data.f9,
        f10 = data.f10
    ,synchronize_session="fetch")
    return data

def increment_url(db:Session,url:HttpUrl) -> Url:
    data = db.query().where(UrlDbModel.url == url).update(appearances = UrlDbModel.appearances + 1,synchronize_session="fetch")
    return data

