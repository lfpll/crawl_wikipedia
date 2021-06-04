from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = os.environ["CONN_STRING"]

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_size=50)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

BaseDbModel = declarative_base()

