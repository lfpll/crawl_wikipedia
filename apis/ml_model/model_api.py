import requests
import os
import json

from fastapi import FastAPI,HTTPException
from os.path import dirname,realpath
from apis.ml_model.model import AppearancesModel
from apis.crud.schemas import Url
app = FastAPI()

dir_path = dirname(realpath(__file__))

# Base url to update or get data 
# POST to update GET to insert
SQL_API_URL = os.environ["SQL_API_URL"]
MODEL_PATH  = "%s/model.pckl"%dir_path
MODEL_OBJ   = AppearancesModel()
MODEL       = MODEL_OBJ.load_model(MODEL_PATH)


@app.get('/appearances/{url:path}',response_model=Url)
async def get_appearances(url:str):
    rest_endpoint = "%s%s"%(SQL_API_URL,url)
    resp = requests.get(rest_endpoint)
    
    # Check if url exists on database
    if resp.status_code != 200:        
        # Adding the columns that the models expect
        df = MODEL_OBJ.add_columns(url)
        dict_format = df.to_dict(orient='records')[0]
        # Updating the  
        appearences = MODEL.predict(df)
        dict_format['appearances'] = appearences[0]
        dict_format['url'] = url
        resp = requests.post(SQL_API_URL,data=json.dumps(dict_format))

        if resp.status_code != 200:
            raise HTTPException(status_code=500,detail="Invalid input, generic")
    return resp.json()