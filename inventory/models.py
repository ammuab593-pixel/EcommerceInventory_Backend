
from django.db import models
from django.contrib.auth.models import User


# 1. Category Model
class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.category_name


# 2. Supplier Model
class Supplier(models.Model):
    supplier_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.supplier_name


# 3. Product Model
class Product(models.Model):
    product_name = models.CharField(max_length=150)

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products'
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name='products'
    )

    vendor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
        null=True,
        blank=True
    )

    description = models.TextField(blank=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock_quantity = models.PositiveIntegerField(default=0)

    reorder_level = models.PositiveIntegerField(default=5)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name

    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.reorder_level


# 4. Stock Movement Model
class StockMovement(models.Model):

    MOVEMENT_CHOICES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    movement_type = models.CharField(
        max_length=3,
        choices=MOVEMENT_CHOICES
    )

    quantity = models.PositiveIntegerField()

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )

    date = models.DateTimeField(auto_now_add=True)

    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.product} - {self.movement_type}"
