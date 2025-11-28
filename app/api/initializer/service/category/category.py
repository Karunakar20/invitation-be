import os
import pandas as pd
from api.models.lovs.category import Category,SubCategory
from core.db.db_config import SessionLocal

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class CategoryInitializer:

      def __init__(self):
            self.db = SessionLocal()
            self.category_model = Category
            self.sub_category_model = SubCategory
    
      def categotyInitializer(self):
            category_path = os.path.join(BASE_DIR, "data/category/category .csv")
            
            categories = pd.read_csv(category_path)

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

      def subCategotyInitializer(self):

            sub_category_path = os.path.join(BASE_DIR, "data/category/sub_category.csv")

            sub_categories = pd.read_csv(sub_category_path)

            for _, sub_category in sub_categories.iterrows():

                  self.category_code = sub_category['category_code']
                  
                  self.sub_cat_name = sub_category['name']
                  self.sub_cat_code = sub_category['code']
                  self.sub_cat_colore_code = sub_category['colore']

                  category = self.db.query(self.category_model).filter(self.category_model.code == self.category_code).first()
                  self.existing_sub_category = self.db.query(self.sub_category_model).filter(self.sub_category_model.code == self.sub_cat_code).first()

                  if self.existing_sub_category:
                        self.existing_sub_category.code = self.sub_cat_code
                        self.existing_sub_category.name = self.sub_cat_name
                        self.existing_sub_category.colore_code = self.sub_cat_colore_code
                        self.existing_sub_category.category_id = category.id

                  else:

                        self.new_category = SubCategory(
                              code=self.sub_cat_code,
                              name=self.sub_cat_name,
                              colore_code=self.sub_cat_colore_code,
                              category_id = category.id
                              )
                        
                        self.db.add(self.new_category)

            self.db.commit()
