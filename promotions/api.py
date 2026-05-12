from ninja import Router
from ninja_jwt.authentication import JWTAuth

from catalog.schemes import ErrorSchema, Successful_message
from promotions.schemes import DiscountSchema, DiscountView, BonusSchema
from promotions.services import create_discount, get_discount, delete_discount, create_bonus

router = Router(tags=['promotions'])


@router.post('promotions/', response={201: Successful_message, 400: ErrorSchema})
def create_discount_(request, data: DiscountSchema):
    return create_discount(request, data.dict())


@router.get('promotions/', response={200: list[DiscountView], 400: ErrorSchema}, auth=JWTAuth())
def get_discount_(request):
    return get_discount(request)


@router.delete('promotions/', response={200: Successful_message, 404: ErrorSchema}, auth=JWTAuth())
def delete_discount_(request, pk: int):
    return delete_discount(request, pk)


@router.post('promotions/bonus/', response={201: Successful_message, 400: ErrorSchema},auth=JWTAuth())
def create_bonus_(request,data: BonusSchema):
    return create_bonus(data.dict())
