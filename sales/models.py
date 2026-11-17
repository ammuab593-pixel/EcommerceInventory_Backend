
from django.db import models
from django.contrib.auth.models import User
from inventory.models import Product


class Sale(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    sold_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )
    sale_date = models.DateTimeField(auto_now_add=True)

    @property
    def total_amount(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"Sale - {self.product.product_name}"


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart - {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['cart', 'product'],
                name='unique_product_per_cart'
            )
        ]

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity}"
