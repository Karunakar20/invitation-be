from sqlalchemy import Column, String, Integer, Boolean, DateTime
from app.core.db.database import Base
from datetime import datetime


class Users(Base):
    __tablename__ = "tb_users"

    id = Column(Integer, primary_key=True, index=True)

    # Common fields
    user_name = Column(String(100), nullable=True)
    email = Column(String(150), unique=True, index=True, nullable=False)

    # Password (only for custom login)
    password = Column(String(255), nullable=True)

    # Auth type
    auth_provider = Column(String(50), default="local")  
    # values: local / google

    # OAuth fields
    oauth_id = Column(String(255), nullable=True)  # Google sub ID
    profile_pic = Column(String(255), nullable=True)

    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)