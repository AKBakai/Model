from django.contrib import admin
from shop.models import User, Product, Sale

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'money',
    )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'nazvaniya',
        'price',
        'amount'
    )

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'product'
    )