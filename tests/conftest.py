import os

from app.auth.routes import get_db

os.environ["ENV"] = "test"

import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import uuid

import pytest
from fastapi.testclient import TestClient
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.models import Base, User

# 🔐 пароль
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🧪 тестовая БД
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# ✅ ФИКСТУРА БД (ОДНА!)
@pytest.fixture(scope="function")
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ клиент
@pytest.fixture
def client():
    return TestClient(app)


# 👤 обычный пользователь
@pytest.fixture
def user_test(db):
    user = User(
        email=f"user{uuid.uuid4()}@test.com",
        hashed_password=pwd_context.hash("123456"),
        role="user",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# 👑 админ
@pytest.fixture
def admin_test(db):
    user = User(
        email=f"admin{uuid.uuid4()}@test.com",
        hashed_password=pwd_context.hash("123456"),
        role="admin",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# 🔑 токен
@pytest.fixture
def get_token(client):
    def _get_token(email, password):
        res = client.post("/login", data={"username": email, "password": password})
        assert res.status_code == 200
        return res.json()["access_token"]

    return _get_token
