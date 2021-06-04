FROM python:3.9.5

COPY ./ /

RUN ["pip","install","--upgrade","pip"]

COPY ./requirements.txt /app
RUN pip install -r requirements.txt


CMD ["sleep","36000000000"]
