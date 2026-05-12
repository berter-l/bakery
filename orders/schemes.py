from datetime import datetime

from ninja import ModelSchema, Schema, FilterSchema, Field

from orders.models import Order


class OrdersResultSchema(FilterSchema):
    status: str


class OrderUpdateSchema(Schema):
    status: dict[int, str]


class OrderCreateSchema(Schema):
    customer_comment: str
    bonus: int | None = None


class OrderViewSchema(Schema):
    status: str
    total_price: float
    final_price: float
    customer_comment: str
    created_at: datetime
    bonus_count: int

