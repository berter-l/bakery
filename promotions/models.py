from django.contrib.auth.models import User
from django.db import models

from catalog.models import Category


class Discount(models.Model):
    discount_percent = models.PositiveIntegerField(default=0, verbose_name="Скидка %")

    on_all = models.BooleanField(default=False, verbose_name="На все товары")
    category = models.OneToOneField(
        Category,
        on_delete=models.CASCADE,
        related_name='discount',
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True, verbose_name="Активна")
    date_create = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Скидка"


class Bonus(models.Model):
    bonus = models.IntegerField(default=0, verbose_name="% от заказа")


class UserBonus(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='bonus',
        verbose_name="Пользователь"
    )
    balance = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Бонус")
