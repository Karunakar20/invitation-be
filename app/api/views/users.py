from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from app.api.pydentic.users.users import UserCreate, UserGoogleAuth, UserLogin
from app.api.services.users.users import google_auth, login_user, register_user
from app.core.db.db_config import db_connection
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/service",tags=["Users"])

@router.post("/register")
async def register(data: UserCreate, db: AsyncSession = Depends(db_connection)):
    return await register_user(db, data)

@router.post("/login")
async def login(data: UserLogin, db: AsyncSession = Depends(db_connection)):
    return await login_user(db, data)

@router.post("/google")
async def google_login(data: UserGoogleAuth, db: AsyncSession = Depends(db_connection)):
    return await google_auth(db, data)