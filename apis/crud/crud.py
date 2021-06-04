from apis.crud.models import UrlDbModel
from apis.crud.schemas import Url
from sqlalchemy.dialects.postgresql import insert
from pydantic import HttpUrl
from sqlalchemy.orm import Session
from apis.ml_model.model import AppearancesModel

model_obj = AppearancesModel() 

def create_url(db: Session,url:Url):
    new_cols_objs = model_obj.add_columns(url.url).to_dict(orient='records')[0]
    new_cols_objs['url'] = url.url
    new_url = UrlDbModel(**new_cols_objs)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url

def get_url(db:Session, url:HttpUrl):
    return db.query(UrlDbModel.url,UrlDbModel.id,UrlDbModel.appearances,UrlDbModel.is_file,
                    UrlDbModel.is_arabic,UrlDbModel.last_path_length,UrlDbModel.percent_of_letters_path,UrlDbModel.percent_of_numbers_path,
                    UrlDbModel.path_length,UrlDbModel.full_lengh,UrlDbModel.number_of_subpaths,UrlDbModel.related_original_url).where(UrlDbModel.url == url).first()

def update_url(db:Session,url:HttpUrl,data:Url) -> Url:
    data = db.query().where(UrlDbModel.url == url).update(**data,synchronize_session="fetch")
    return data

def increment_url(db:Session,url:HttpUrl) -> Url:
    db.query(UrlDbModel).filter(UrlDbModel.url == url).update({UrlDbModel.appearances: UrlDbModel.appearances + 1},synchronize_session="fetch")
    db.commit()
    return get_url(db,url)
