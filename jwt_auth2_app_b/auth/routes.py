from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from jwt_auth2_app_b.database import SessionLocal
from jwt_auth2_app_b.models import User
from jwt_auth2_app_b.auth.schemas import UserCreate
from jwt_auth2_app_b.auth.jwt import create_access_token
from jwt_auth2_app_b.dependencies import get_current_user

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(db, email):
    return db.query(User).filter(User.email == email).first()


# 🔐 REGISTER
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user(db, user.email):
        raise HTTPException(400, "User already exists")

    hashed_password = pwd_context.hash(user.password)

    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()

    return {"msg": "User created"}


# 🔐 LOGIN
@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, user.email)

    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(400, "Invalid credentials")

    token = create_access_token({"sub": user.email})

    return {"access_token": token, "token_type": "bearer"}


# 🔒 PROTECTED
@router.get("/protected")
def protected(current_user=Depends(get_current_user)):
    return {"msg": f"Hello {current_user['sub']}"}
