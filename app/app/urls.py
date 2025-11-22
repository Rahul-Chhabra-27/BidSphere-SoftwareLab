from django.urls import path
from .views import (
    CategoryView,
    ProductView,
    ProductsByCategoryView,
    ProductDetailView,
)

urlpatterns = [
    path("categories/", CategoryView.as_view(), name="categories-list-create"),
    path("products/", ProductView.as_view(), name="products-list-create"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("products/category/<str:category_name>/", ProductsByCategoryView.as_view(), name="products-by-category"),
]
