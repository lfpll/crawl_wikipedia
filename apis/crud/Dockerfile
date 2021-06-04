FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./ /app/apis
COPY ./requirements.txt /app

RUN ["pip","install","-r","requirements.txt"]

CMD ["uvicorn", "apis.crud.crud_api:app", "--host", "0.0.0.0", "--port", "80"]
