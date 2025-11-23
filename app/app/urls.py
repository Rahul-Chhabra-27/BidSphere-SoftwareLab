from django.urls import path
from .views import (
    CategoryView,
    ProductView,
    ProductsByCategoryView,
    ProductDetailView,
)
from .auth_view import RegisterView, LoginView
from .payment_view import VerifyPaymentView
from .order_view import CreateOrderView
urlpatterns = [
    path("categories/", CategoryView.as_view(), name="categories-list-create"),
    path("products/", ProductView.as_view(), name="products-list-create"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("products/category/<str:category_name>/", ProductsByCategoryView.as_view(), name="products-by-category"),
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("create-order/", CreateOrderView.as_view(), name="create-order"),
    path("verify-payment/", VerifyPaymentView.as_view(), name="verify-payment"),
]
