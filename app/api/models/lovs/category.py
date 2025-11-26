from sqlalchemy import Column, String, Integer, ForeignKey
from core.db.database import Base

class Category(Base):

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(5))
    name = Column(String(30))
    colore = Column(String(10), nullable=True)

    __tablename__ = "tb_category"
    
class SubCategory(Base):

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("tb_category.id"))
    code = Column(String(5))
    colore = Column(String(10), nullable=True)

    __tablename__ = "tb_sub_category"