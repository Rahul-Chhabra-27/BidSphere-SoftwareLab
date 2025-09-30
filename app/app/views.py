# views.py
from django.shortcuts import render, get_object_or_404
from .models import Product  

def product(request):

    products = Product.objects.all()

    context = {
        'products': products
    }
    return render(request, 'products/product_detail.html', context)