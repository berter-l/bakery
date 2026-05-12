from time import sleep
from typing import Any

from django.db import transaction
from ninja.errors import ValidationError

from catalog.models import Product, Category
from catalog.schemes import SearchResultSchema
from promotions.services import add_category_bonus


def error_exists(data: dict, model, not_to=None):
    errors = {}
    for key in data:
        if not_to is not None:
            if key in not_to:
                continue
        d = {key: data[key]}
        if model.objects.filter(**d).exists():
            errors[key] = f"{key} already exists"
    if errors:
        return errors


def get_all_objects(model):
    return model.objects.all()


def search_product(filters: SearchResultSchema) -> Product:
    products = Product.objects.all().select_related('category').only(
        'price',
        'name',
        'price',
        'category__name',
        'stock',
        'slug',
        'image'
    )
    products = filters.filter(products)
    return products


def get_one_product(slug: str):
    try:
        object = Product.objects.get(slug=slug)
        return 200, object
    except Product.DoesNotExist:
        return 404, {'message': 'Product not found'}


def create_product(data: dict):
    error = error_exists(data, Product, ['category_id', 'image', 'default_price', 'stock'])
    if error:
        return 404, {'message': error}
    else:
        try:
            with transaction.atomic():
                product = Product(**data)
                new_price = add_category_bonus(pk=product.category_id, flag=True)
                if new_price:
                    product.price = product.default_price - (product.default_price * (new_price / 100))
                    product.save()
                else:
                    product.price = product.default_price
                product.save()
                return 200, {'message': 'Product created'}
        except:
            raise
            return 500, {'message': 'При создании продукта произошла ошибка.'
                                    ' Пожалуйста, повторите попытку позже.'}


def create_category(data: dict) -> tuple[int, dict[str, dict[Any, Any]]] | tuple[int, dict[str, str]]:
    error = error_exists({'name': data['name']}, Category)
    if error:
        return 404, {'message': error}

    try:
        with transaction.atomic():
            category = Category.objects.create(**data)
            return 200, {'message': 'Category created'}

    except Exception:
        return 500, {'message': 'При создании категории произошла ошибка.'
                                ' Пожалуйста, повторите попытку позже.'}


def delete_product(slug: str):
    try:
        with transaction.atomic():
            product = Product.objects.get(slug=slug)
            product.delete()
            return 200, {'message': 'Product deleted'}
    except Product.DoesNotExist:
        return 404, {'message': 'Product not found'}


def delete_category(slug: str):
    try:
        with transaction.atomic():
            category = Category.objects.get(slug=slug)
            category.delete()
            return 200, {'message': 'Category deleted'}
    except Category.DoesNotExist:
        return 404, {'message': 'Category not found'}


def update_product(slug: str, data: dict):
    flag = False
    try:
        product = Product.objects.get(slug=slug)
        with transaction.atomic():
            if product.default_price != data['default_price'] and data['default_price'] is not None:
                flag = True
                dew = data['default_price']
            for x in data:

                if flag:

                    new_price = add_category_bonus(pk=product.category_id, flag=True)
                    product.price = dew - (dew * (new_price / 100))

                setattr(product, x, data[x])

            product.save()
            return 200, {'message': 'Product updated'}

    except Product.DoesNotExist:
        return 404, {'message': 'Product not found'}


def update_category(slug: str, data: dict[str, str]):
    try:
        with transaction.atomic():
            category = Category.objects.get(slug=slug)
            for x in data:
                setattr(category, x, data[x])
            category.save()
            return 200, {'message': 'Category updated'}
    except Category.DoesNotExist:
        return 404, {'message': 'Category not found'}


def get_categories_product(pk):
    data = Product.objects.filter(category_id=pk)
    return data


def update_quantity(product, quantity: dict):
    error = {}
    update_list = []
    for item in product:
        if item.stock < quantity[item.id]:
            error[
                item.name] = f'Для продукта {item.name} вы хотите заказать {quantity[item.id]} но доступно {item.stock} .'
        else:
            item.stock -= quantity[item.id]
            item.sold_count += quantity[item.id]
            update_list.append(item)
    if error:
        return error
    else:
        Product.objects.bulk_update(update_list, ['stock', 'sold_count'])
        return []
