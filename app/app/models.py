from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User
from app.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=20, default="PENDING")  # PENDING / PAID / FAILED
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payment")
    razorpay_payment_id = models.CharField(max_length=200)
    razorpay_signature = models.CharField(max_length=200)
    status = models.CharField(max_length=20, default="SUCCESS")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.status}"