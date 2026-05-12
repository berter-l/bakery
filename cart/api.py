from ninja import Router

from cart.schemes import CartViewSchema, CartViewSchemaTotal
from cart.services import all_cart, add_cart, delete_all_cart, delete_one_cart
from catalog.schemes import Successful_message, ErrorSchema
from ninja_jwt.authentication import JWTAuth
router = Router(tags=['cart'])


@router.get('/cart/', response={200: CartViewSchemaTotal, 500: ErrorSchema},auth=JWTAuth())
def all_carts(request):
    return all_cart(request)


@router.post('/cart/add/', response={200: Successful_message, 404: ErrorSchema},auth=JWTAuth())
def add_cart_(request, slug: str):
    return add_cart(request, slug)


@router.delete('/cart/all/delete/', response={200: Successful_message, 404: ErrorSchema},auth=JWTAuth())
def delete_all_cart_(request):
    return delete_all_cart(request)


@router.delete('/cart/one/delete/', response={200: Successful_message, 404: ErrorSchema},auth=JWTAuth())
def delete_one_cart_(request, slug: str):
    return delete_one_cart(request, slug=slug)
