from api.models.lovs.catalog.category import SubCategory
from core.db.db_config import SessionLocal
from api.utilities.common import Response,ResponseType

class SubCategoryLovService:
      def __init__(self):
            self.db = SessionLocal() 

      def getSubCategory(self,pData):
            category_id = pData.get('category_id')
            search = pData.get('search')
            try:
                  self.sub_category = self.db.query(SubCategory)
                  if category_id:
                        self.sub_category = self.sub_category.filter(SubCategory.category_id == category_id)
                  
                  if search:
                        self.sub_category = self.sub_category.filter(SubCategory.name.ilike(f"%{search}%"))

                  sub_category_list = []
                  for sub_category in self.sub_category:

                        data = {
                              "id": sub_category.id,
                              "icon_name": sub_category.code,
                              "name": sub_category.name,
                              "colore_code": sub_category.colore_code
                        }
                        sub_category_list.append(data)
                  return Response(True,ResponseType.success,None,None,sub_category_list)
            
            except Exception as e:
                  return Response(False,ResponseType.err,"Unable to retrive sub category",str(e))

