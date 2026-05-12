from ninja import ModelSchema, Schema, FilterSchema, Field
from pydantic import BaseModel, field_validator
from ninja.errors import ValidationError

from cart.models import CartItem, Cart


class CartItemSchemaCreate(ModelSchema):
    class Meta:
        model = CartItem
        fields = '__all__'


class CartSchema(ModelSchema):
    class Meta:
        model = Cart
        fields = '__all__'


class CartViewSchema(Schema):
    price: int
    product__name: str
    quantity: int


class CartViewSchemaTotal(Schema):
    carts: list[CartViewSchema]
    total_price: float