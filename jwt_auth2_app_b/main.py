from fastapi import FastAPI
from jwt_auth2_app_b.database import Base, engine
from jwt_auth2_app_b.auth.routes import router as auth_router

jwt_auth2_app_b = FastAPI()

Base.metadata.create_all(bind=engine)

jwt_auth2_app_b.include_router(auth_router)