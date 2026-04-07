import os

os.environ["ENV"] = "test"

import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
import uuid
from fastapi.testclient import TestClient
from app.database import SessionLocal
from app.main import app
from app.models import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from app.database import Base, engine


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def db():
    db = SessionLocal()
    yield db
    db.close()


@pytest.fixture
def user_test(db):
    user = User(
        email=f"user{uuid.uuid4()}@test.com",
        hashed_password=pwd_context.hash("123456"),
        role="user"
    )
    db.add(user)
    db.commit()
    return user


@pytest.fixture
def admin_test(db):
    user = User(
        email=f"admin{uuid.uuid4()}@test.com",
        hashed_password=pwd_context.hash("123456"),
        role="admin"
    )
    db.add(user)
    db.commit()
    return user


@pytest.fixture
def get_token(client):
    def _get_token(email, password):
        res = client.post("/login", data={
            "username": email,
            "password": password
        })
        assert res.status_code == 200
        return res.json()["access_token"]

    return _get_token
