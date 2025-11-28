from sqlalchemy import Column, String, Integer
from core.db.database import Base

class Users(Base):
      id = Column(Integer, primary_key=True, index=True)
      user_name = Column(String(50))
      password = Column(String(50))

      __tablename__ = "tb_users"