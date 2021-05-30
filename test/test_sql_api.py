import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient
from apis.crud_api import app,get_db
from apis.db import BaseDbModel


client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

BaseDbModel.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def mock_db():
    pass

def test_get_url_information():
    response = client.get()
    pass


def test_create_url_endpoint():
    pass


def test_update_url_endpoint():
    pass


def test_increment_url():
    pass

