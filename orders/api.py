from typing import Any

from ninja import Router, Query

from catalog.schemes import ErrorSchema, Successful_message
from orders.schemes import OrdersResultSchema, OrderCreateSchema, OrderViewSchema, OrderUpdateSchema
from orders.services import create_order, get_all_orders, search_orders, update_order
from ninja_jwt.authentication import JWTAuth
from ninja.pagination import paginate, PageNumberPagination, LimitOffsetPagination
from ninja.pagination import paginate, PaginationBase
router = Router(tags=['orders'])


@router.post("/orders/", response={201: Successful_message, 500: ErrorSchema}, auth=JWTAuth())
def orders(request, data: OrderCreateSchema):
    return create_order(request, data.dict())


@router.get("/orders/", response={200: list[OrderViewSchema], 404: ErrorSchema}, auth=JWTAuth())
def all_orders(request):
    return get_all_orders(request)


@router.get("/search/orders/", response=list[OrderViewSchema], auth=JWTAuth())
@paginate(PageNumberPagination, page_size=10)
def search_orders_(request, filters: OrdersResultSchema = Query(...)):
    return search_orders(request, filters)


@router.patch("/orders/", response={201: Successful_message, 404: ErrorSchema}, auth=JWTAuth())
def update_order_(request, data: OrderUpdateSchema):
    return update_order(data.dict())
