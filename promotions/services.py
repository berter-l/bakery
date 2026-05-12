from django.db import transaction

from catalog.models import Product
from promotions.models import Discount, Bonus, UserBonus


def create_discount(request, data):
    discount = Discount.objects.filter(on_all=True)
    if discount.exists():
        return 400, {'message': 'Сначала удали скидку на все продукты.'}
    elif (data['category'] is not None and data['on_all']) or data['discount_percent'] > 100:
        return 400, {'message': 'dsssd'}
    try:

        with transaction.atomic():
            if data['on_all']:
                product = Product.objects.all().only('price', 'default_price')
                items = Discount.objects.all().only('id')
                items.delete()

            else:
                discount = Discount.objects.filter(category_id=data['category'])
                if discount.exists():
                    return 400, {'message': 'Discount already exists'}

            Discount.objects.create(
                on_all=data['on_all'],
                category_id=data['category'],
                discount_percent=data['discount_percent'],
                is_active=data['is_active']
            )
            if data['on_all']:
                add_all_bonus(product)
            else:
                add_category_bonus(data['category'], data=product)
            return 201, {'message': 'Discount created'}


    except:
        raise
        return 400, {'message': 'Discount not found'}


def get_discount(request):
    data = Discount.objects.all().select_related('category')
    if data.exists():
        return 200, data
    else:
        return 400, {'message': 'Discount not found'}


def get_one_discount(request):
    data = Discount.objects.filter()


def delete_discount(request, pk):
    try:

        with transaction.atomic():
            product = Discount.objects.filter(id=pk).only('category_id')

            data = Product.objects.filter(category_id=product[0].category_id).only('price', 'default_price')
            product.delete()

            update_price_to_default(data)
            return 200, {'message': 'Product deleted'}
    except Discount.DoesNotExist:
        return 404, {'message': 'Product not found'}


def chet(data, proc):
    if type(proc) is dict:
        procent = [proc[x] for x in proc]
    else:
        procent = proc
    update_list = []
    if len(proc) == 1:
        for item in data:
            item.price = round(float(item.default_price) - (float(item.default_price) * (procent[0] / 100)), 2)
            update_list.append(item)
        Product.objects.bulk_update(update_list, ['price'])
        return data
    else:

        for item in data:
            item.price = round(float(item.default_price) - (float(item.default_price) * (proc[item.category_id] / 100)),
                               2)
            update_list.append(item)
        Product.objects.bulk_update(update_list, ['price'])
        return data


def add_all_bonus(data):
    check = Discount.objects.all().only('on_all', 'discount_percent')
    on_all_check = [x.discount_percent for x in check if x.on_all]
    return chet(data, on_all_check)


def add_category_bonus(pk, data=None, flag=False):
    check = Discount.objects.all().only('on_all', 'category_id', 'discount_percent')
    on_all_check = [x.discount_percent for x in check if x.on_all]
    pk_check = {x.category_id: x.discount_percent for x in check if x.category_id == pk}
    if on_all_check and flag:
        return on_all_check[0]
    if pk_check and flag:
        return pk_check[pk]
    if flag:
        return 0
    if pk_check:
        return chet(data, pk_check)
    else:
        return chet(data, on_all_check)


def update_price_to_default(data):
    update_list = []
    for item in data:
        item.price = item.default_price
        update_list.append(item)
    Product.objects.bulk_update(update_list, ['price'])


def update_balance(request, total_price, bonus_price=None):
    bonus = Bonus.objects.all().first()
    if bonus is not None:
        bonus = bonus.bonus
    else:

        bonus = 0
    try:
        user_bonus = UserBonus.objects.get(user=request.user)
        if bonus_price == 0:
            user_bonus.balance = float(user_bonus.balance) + (float(total_price) * (float(bonus) / 100))
            user_bonus.save()
            return total_price
        else:
            if bonus_price <= float(user_bonus.balance):
                user_bonus.balance -= bonus_price
                total_price -= bonus_price
                user_bonus.balance = float(user_bonus.balance) + (float(total_price) * (float(bonus) / 100))
                user_bonus.save()
                return total_price
            else:
                raise Exception('Bonus price is less than bonus price')
    except UserBonus.DoesNotExist:
        user_bonus = UserBonus(user=request.user, balance=float(float(total_price) * (float(bonus) / 100)))
        user_bonus.save()
        return total_price


def create_bonus(data):
    if Bonus.objects.exists():
        return 400, {'message': 'сначала удалите текущий бонус'}
    else:
        Bonus.objects.create(**data)
        return 201, {'message': 'Bonus created'}
