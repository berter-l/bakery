from ninja import ModelSchema, Schema, FilterSchema, Field

from promotions.models import Discount


class DiscountSchema(ModelSchema):
    category: int = None

    class Meta:
        model = Discount
        exclude = ('id', 'date_create')


class DiscountView(Schema):
    discount_percent: int
    on_all: bool
    is_active: bool
    category__name: str = None


class BonusSchema(Schema):
    bonus: int
