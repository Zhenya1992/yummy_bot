from django.contrib import admin
from .models import Users, Categories, Products


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    """Класс пользователей для админ-панели"""

    list_display = ('id', 'name', 'telegram', 'phone')
    search_fields = ('name', 'phone')
    ordering = ['id']


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    """Класс категорий для админ-панели"""

    list_display = ('id', 'category_name')
    search_fields = ('id',)
    ordering = ['id']


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    """Класс товаров для админ-панели"""

    list_display = ('id', 'product_name', 'description', 'image', 'price', 'category')
    search_fields = ('id', 'price', 'category')
    ordering = ['id']