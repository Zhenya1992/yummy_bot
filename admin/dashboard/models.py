from django.db import models


class User(models.Model):
    """Класс для хранения информации о пользователях"""

    name = models.CharField(max_length=50)
    telegram = models.BigIntegerField(unique=True, )
    phone = models.CharField(max_length=15, null=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    def __str__(self):
        return self.name


class Categories(models.Model):
    """Класс для хранения информации о категориях"""

    category_name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

    def __str__(self):
        return self.category_name


class Products(models.Model):
    """Класс для хранения информации о товарах"""

    product_name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    images = models.ImageField(upload_to='media/', blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='products')

    class Meta:
        db_table = 'products'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['id']

    def __str__(self):
        return self.product_name