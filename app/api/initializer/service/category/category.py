import pandas as pd
from api.models.lovs.category import Category,SubCategory
from core.db.db_config import SessionLocal

class CategoryInitializer:

      def __init__(self):
            self.db = SessionLocal()
            self.category_model = Category
            self.sub_category_model = SubCategory
    
      def initializer(self):
            
            categories = pd.read_csv("app/api/initializer/data/category/category .csv")

            for _, category in categories.iterrows():
                  self.code = category['code']
                  self.name = category['name']
                  self.colore_code = category['colore']

                  self.existing_category = self.db.query(self.category_model).filter(self.category_model.code == self.code).first()

                  if self.existing_category:
                        self.existing_category.code = self.code
                        self.existing_category.name = self.name
                        self.existing_category.colore_code = self.colore_code
                  else:
                        self.new_category = Category(
                              code=self.code,
                              name=self.name,
                              colore_code=self.colore_code
                              )
                        
                        self.db.add(self.new_category)

            self.db.commit()
            






if __name__ == "__main__":
    CategoryInitializer().initializer()
