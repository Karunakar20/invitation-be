from fastapi import APIRouter

from api.services.lovs.catalog.category import CategoryLovService
from api.services.lovs.catalog.sub_category import SubCategoryLovService

router = APIRouter(prefix="/lovs",tags=["lovs"])

@router.get("/category/")
def get_category(search: str | None = None):
    cRes = CategoryLovService().getCategory(search)
    return cRes.toJson()

@router.get("/sub_category/")
def get_sub_category(category_id: int, search: str | None = None):

    data = {
        "search":search,
        "category_id":category_id
    }
    sRes = SubCategoryLovService().getSubCategory(data)
    return sRes.toJson()

