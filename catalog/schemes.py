from django.db.models import Q
from ninja import ModelSchema, Schema, FilterSchema, Field
from pydantic import BaseModel, field_validator
from catalog.models import Product, Category
from ninja.errors import ValidationError


class ProductSchema(Schema):
    category_id: int | None = None
    name: str | None = None
    image: str | None = None
    description: str | None = None
    default_price: float | None = None
    stock: int | None = None


class ProductViewSchema(Schema):
    name: str
    price: float
    stock: int
    image: str | None


class Category_product_Schema(ProductSchema):
    category_id: int


class ErrorSchema(Schema):
    message: str | dict[str, str]


class Successful_message(ErrorSchema):
    pass


class SearchResultSchema(FilterSchema):
    is_new: bool = False
    min_price: float | None = None
    max_price: float | None = None
    name: str | None = None
    category: str | None = None
    in_stock: bool | None = None
    is_new: bool | None = None

    def custom_expression(self) -> Q:
        q = Q()
        if self.is_new:
            q &= Q(is_new=self.is_new)
        if self.min_price:
            q &= Q(price__gte=self.min_price)
        if self.max_price:
            q &= Q(price__lte=self.max_price)
        if self.name:
            q &= Q(name__icontains=self.name)
        if self.category:
            q &= Q(category__name=self.category)
        if self.in_stock:
            q &= Q(stock__gt=0)
        if self.is_new:
            q &= Q(is_new=self.is_new)
        return q


class CategorySchema(Schema):
    name: str | None
    is_active: bool | None = None
