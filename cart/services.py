from typing import Any

from django.db.models import Sum
from catalog.models import Product
from catalog.services import get_one_product
from .models import Cart, CartItem
from django.db.models import Count


def get_cart(request) -> Any:
    try:
        cart = Cart.objects.get(user=request.user)
        return cart
    except Cart.DoesNotExist:
        raise


def all_cart(request,flag=False) -> Any | None:
    try:

        data = get_cart(request)
        new_data = data.items.values('product__name', 'product').annotate(price=Sum('product__price'),
                                                                          quantity=Count('product'))
        total = sum([x['price'] for x in new_data])
        return {'carts': new_data,
                'total_price': total,
                'data': data}
    except Cart.DoesNotExist:
        if flag:
            raise
        return 500, {'message': 'Cart not found'}


def add_cart(request, slug: str) -> Any | None:
    product = get_one_product(slug)[1]

    try:
        data = get_cart(request)
        cart = CartItem.objects.create(cart=data, product=product)
        return 200, {'message': 'Cart Added!'}
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
        cart_item = CartItem.objects.create(cart=cart, product=product)
        return 200, {'message': 'Cart Added!'}


def delete_all_cart(request, cart=None) -> Any:
    if cart is None:
        try:
            data = get_cart(request)
            data.delete()
            return 200, {'message': 'Cart Deleted!'}
        except Cart.DoesNotExist:
            return 404, {'message': 'Cart not found'}
    else:
        cart.delete()


def delete_one_cart(request, slug: str) -> Any:
    try:
        cart = get_cart(request).items.filter(product__slug=slug).first()
        cart.delete()
        return 200, {'message': 'Cart Deleted!'}
    except Cart.DoesNotExist:
        return 404, {'message': 'Cart not found'}
