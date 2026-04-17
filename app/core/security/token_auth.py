from jose import jwt
from datetime import datetime, timedelta

from core.config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.jwt_algorithm

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)