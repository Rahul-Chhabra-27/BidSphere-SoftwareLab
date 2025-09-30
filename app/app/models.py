# models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)        # Name of the product
    description = models.TextField(blank=True)    # Optional description
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price with 2 decimals
    stock = models.PositiveIntegerField(default=0)  # Number of items in stock
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when created
    updated_at = models.DateTimeField(auto_now=True)      

    def __str__(self):
        return self.name