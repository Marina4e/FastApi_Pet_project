from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

from app.database import SessionLocal
from app.models import User
from app.auth.schemas import UserCreate
from app.auth.jwt import create_access_token, create_refresh_token
from app.dependencies import get_current_user
from app.auth.jwt import verify_token

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 📌 DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 📌 get user
def get_user(db, email: str):
    return db.query(User).filter(User.email == email).first()


# ✅ REGISTER (залишається як є)
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user(db, user.email):
        raise HTTPException(status_code=400, detail="User exists")

    new_user = User(
        email=user.email,
        hashed_password=pwd_context.hash(user.password),
        role=user.role if user.role else "user"
    )

    db.add(new_user)
    db.commit()

    return {"msg": "User created"}


@router.post("/login")
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    email = form_data.username
    password = form_data.password

    db_user = get_user(db, email)

    if not db_user or not pwd_context.verify(password,
                                             db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token({
        "sub": email,
        "role": db_user.role
    })

    refresh_token = create_refresh_token({"sub": email})

    return {
        "access_token": access_token,
        "refresh_token_value": refresh_token,
        "token_type": "bearer"
    }


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "email": current_user.email,
        "role": current_user.role
    }


@router.post("/refresh")
def refresh_token(refresh_token_value: str):
    payload = verify_token(refresh_token_value)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    email = payload.get("sub")

    new_access_token = create_access_token({
        "sub": email
    })

    return {"access_token": new_access_token}
