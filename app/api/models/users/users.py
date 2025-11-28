from sqlalchemy import Column, String, Integer, ForeignKey,Date,Time,Boolean
from core.db.database import Base

class Users(Base):
      id = Column(Integer, primary_key=True, index=True)

      __tablename__ = "tb_users"