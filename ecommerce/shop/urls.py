# shop/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('register-payment/<int:order_id>/', views.register_payment, name='register_payment'),
    path('payment-success/<int:order_id>/', views.payment_success, name='payment_success'),
]
