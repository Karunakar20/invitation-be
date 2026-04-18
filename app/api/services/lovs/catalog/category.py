from app.core.db.db_config import SessionLocal
from app.api.models.lovs.catalog.category import Category
from app.api.utilities.common import Response,ResponseType

class CategoryLovService:
      def __init__(self):
            self.db = SessionLocal()

      def getCategory(self,search):
            try:
                  self.category = self.db.query(Category)

                  if search:
                        self.category = self.category.filter(Category.name.ilike(f"%{search}%"))
                  else:
                        self.category = self.category.all()

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

