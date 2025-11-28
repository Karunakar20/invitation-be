from app.api.models.lovs.catalog.category import Category
from core.db.db_config import SessionLocal
from utilities.common import Response,ResponseType

class CategoryLovService:
      def __init__(self):
            self.db = SessionLocal()

      def getCategory(self):
            try:
                  self.category = self.db.query(Category).all()
                  category_list = []
                  for category in self.category:
                        data = {
                              "id": category.id,
                              "name": category.name,
                              "icon_name": category.code,
                              "colore_code": category.colore_code
                        }

                        category_list.append(data)

                  return Response(True,ResponseType.success,None,None,category_list)
            
            except Exception as e:
                  return Response(False,ResponseType.err,"Unable to retrive category",str(e))

