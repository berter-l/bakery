from ninja import Query
from ninja import Router, NinjaAPI
from catalog.models import Product, Category
from catalog.schemes import ProductSchema, ErrorSchema, Category_product_Schema, Successful_message, SearchResultSchema, \
    CategorySchema, ProductViewSchema
from catalog.services import get_all_objects, get_one_product, create_product, delete_product, \
    update_product, search_product, create_category, delete_category, update_category, get_categories_product
from ninja.errors import ValidationError
from ninja_jwt.authentication import JWTAuth
from ninja.pagination import paginate, PageNumberPagination, LimitOffsetPagination

router = Router(tags=['catalog'])


@router.get('/products/', response=list[ProductViewSchema])
@paginate(PageNumberPagination, page_size=10)
def all_products(request) -> list[ProductViewSchema]:
    return get_all_objects(Product)


@router.get('/products/{slug}/', response={200: ProductSchema, 404: ErrorSchema})
def single_product(request, slug) -> ProductSchema:
    return get_one_product(slug)


@router.post('/products/', response={200: Successful_message, 404: ErrorSchema}, auth=JWTAuth())
def create(request, data: Category_product_Schema) -> ProductSchema:
    return create_product(data.dict())


@router.delete('/products/{slug}/', response={200: Successful_message, 404: ErrorSchema}, auth=JWTAuth())
def delete_product_(request, slug):
    return delete_product(slug=slug)


@router.patch('/products/{slug}/', response={200: Successful_message, 404: ErrorSchema}, auth=JWTAuth())
def update_product_(request, slug, data: ProductSchema):
    return update_product(slug=slug, data=data.dict(exclude_unset=True))


@router.get('search/', response=list[ProductSchema])
@paginate(PageNumberPagination, page_size=10)
def search(request, filters: SearchResultSchema = Query(...)):
    return search_product(filters)


@router.get('/categories/', response=list[CategorySchema])
def get_categories(request) -> list[CategorySchema]:
    return get_all_objects(Category)


@router.post('/categories/', response={200: Successful_message, 404: ErrorSchema}, auth=JWTAuth())
def create_category_(request, data: CategorySchema) -> tuple[int, dict[str, str]]:
    return create_category(data.dict())


@router.delete('/categories/{slug}/', response={200: Successful_message, 404: ErrorSchema}, auth=JWTAuth())
def delete_category_(request, slug):
    return delete_category(slug=slug)


@router.patch('/categories/{slug}/', response={200: Successful_message, 404: ErrorSchema}, auth=JWTAuth())
def update_category_(request, slug, data: CategorySchema):
    return update_category(slug=slug, data=data.dict())


@router.get('/category/product/{pk}/', response=list[ProductSchema])
@paginate(PageNumberPagination, page_size=10)
def get_categories_product_(request, pk: int) -> list[ProductSchema]:
    return get_categories_product(pk=pk)
