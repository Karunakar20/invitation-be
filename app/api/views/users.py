from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from app.api.pydentic.users.users import UserCreate, UserGoogleAuth, UserLogin
from app.api.services.users.users import google_auth, login_user, register_user
from app.core.db.db_config import db_connection

router = APIRouter(tags=["Users"])

@router.post("/register")
def register(data: UserCreate, db: Session = Depends(db_connection)):
    return register_user(db, data)

@router.post("/login")
def login(data: UserLogin, db: Session = Depends(db_connection)):
    return login_user(db, data)

@router.post("/google")
def google_login(data: UserGoogleAuth, db: Session = Depends(db_connection)):
    return google_auth(db, data)