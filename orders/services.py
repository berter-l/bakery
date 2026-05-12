from sys import flags

from django.db import transaction

from cart.services import all_cart, delete_all_cart
from catalog.models import Product
from catalog.services import update_quantity
from orders.models import Order, OrderItem
from orders.schemes import OrdersResultSchema, OrderCreateSchema
from promotions.services import update_balance
from ninja import Status


def create_order(request, data: OrderCreateSchema):
    try:
        with transaction.atomic():
            cart_items = all_cart(request,flag=True)
            final_price = update_balance(request, cart_items['total_price'], data['bonus'])
            product_id_ = [item['product'] for item in cart_items['carts']]
            product = Product.objects.filter(pk__in=product_id_)
            quantity = {item['product']: item['quantity'] for item in cart_items['carts']}
            er = update_quantity(product, quantity)
            if er:
                return 500, {'message': er}
            order = Order.objects.create(
                user_id=request.user.id,
                status='pending',
                total_price=cart_items['total_price'],
                final_price=final_price,
                customer_comment=data['customer_comment'],
                bonus_count=data['bonus']
            )

            order_item = []
            for item in cart_items['carts']:
                order_item.append(OrderItem(
                    order=order,
                    product_id=item['product'],
                    quantity=item['quantity'],
                    price=item['price']
                ))
            OrderItem.objects.bulk_create(order_item)
            delete_all_cart(request, cart_items['data'])
        return 201, {'message': 'Order Created'}
    except Exception as err:

        return 500, {'message': str(err)}


def get_all_orders(request):
    data = Order.objects.filter(user_id=request.user.id)
    if data.exists():
        return 200, data
    else:
        return 404, {'message': 'Order Not Found'}


def search_orders(request, filters: OrdersResultSchema) -> Order:
    orders = Order.objects.filter(user=request.user)
    return filters.filter(orders)


def update_order(data):
    data = data['status']
    if len(data) == 0:
        return 404, {'message': 'Order Not Found'}
    i = [x for x in data]
    print(i)
    if len(data) == 1:
        order = Order.objects.get(pk=i[0])
        order.status = data[i[0]]
        order.save()
        return 201, {'message': 'Order Updated'}
    if len(data) >= 2:
        order = Order.objects.filter(pk__in=i).only('id', 'status')
        update_list = []
        for item in order:
            item.status = data[item.id]
            update_list.append(item)
        Order.objects.bulk_update(update_list, ['status'])
        return 201, {'message': 'Order Updated'}
    return None
