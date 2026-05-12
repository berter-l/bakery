from django.contrib import admin
from django import forms
from catalog.models import Product
from promotions.models import Discount, UserBonus, Bonus
from promotions.services import update_price_to_default, add_all_bonus, add_category_bonus


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        on_all = cleaned_data.get("on_all")
        if on_all and category is not None:
            raise forms.ValidationError("You can't add a discount with this category.")


class DiscountAdmin(admin.ModelAdmin):
    form = DiscountForm

    def delete_queryset(self, request, queryset):
        i = []
        for discount in queryset:
            if not discount.on_all:
                i.append(discount.category_id)
        if i:

            data = Product.objects.filter(category_id__in=i).only('price', 'default_price')
            queryset.delete()
            update_price_to_default(data)
        else:
            data = Product.objects.all()
            queryset.delete()
            update_price_to_default(data)

    def save_model(self, request, obj, form, change):
        if obj.on_all and obj.category is None:

            product = Product.objects.all().only('price', 'default_price')
            items = Discount.objects.all().only('id')
            items.delete()
            super().save_model(request, obj, form, change)
            add_all_bonus(product)
        else:
            items = Discount.objects.filter(on_all=True).only('id')
            items.delete()
            product = Product.objects.filter(category_id=obj.category_id).only('price', 'default_price')
            super().save_model(request, obj, form, change)
            add_category_bonus(pk=obj.category_id, data=product)


admin.site.register(Discount, DiscountAdmin)
admin.site.register(UserBonus)
admin.site.register(Bonus)
