from app.api.models.lovs.catalog.category import SubCategory
from core.db.db_config import SessionLocal
from utilities.common import Response,ResponseType

class CategoryLovService:
      def __init__(self):
            self.db = SessionLocal() 

      def getSubCategory(self,id):
            try:
                  self.sub_category = self.db.query(SubCategory).filter(SubCategory.category_id == id).first()

                  data = {
                        "id": self.sub_category.id,
                        "icon_name": self.sub_category.code,
                        "name": self.sub_category.name,
                        "colore_code": self.sub_category.colore_code
                  }
                  return Response(True,ResponseType.success,None,None,data)
            
            except Exception as e:
                  return Response(False,ResponseType.err,"Unable to retrive sub category",str(e))

