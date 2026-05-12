from sys import flags

from django.contrib import admin

from catalog.models import Product, Category
from promotions.services import add_category_bonus


class ProductAdmin(admin.ModelAdmin):
    class Meta:
        model = Product
        fields = '__all__'

    def save_model(self, request, obj, form, change):
        print(add_category_bonus(pk=obj.category_id, flag=True))
        obj.price = float(obj.price) - (float(obj.price) * (add_category_bonus(obj.category_id, flag=True) / 100))
        super().save_model(request, obj, form, change)


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
