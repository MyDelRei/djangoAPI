
# Create your views here.

# shop/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem, Order, Payment

def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

#@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

#@login_required
def cart_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    total_price = sum(item.total_price() for item in cart.items.all())
    return render(request, 'shop/cart.html', {'cart': cart, 'total_price': total_price})

#@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    total_price = sum(item.total_price() for item in cart.items.all())
    if request.method == "POST":
        # Create an order
        order = Order.objects.create(user=request.user, total_price=total_price)
        # Clear the cart
        cart.items.all().delete()
        return redirect('register_payment', order_id=order.id)
    return render(request, 'shop/checkout.html', {'total_price': total_price})

#@login_required
def register_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == "POST":
        payment_method = request.POST.get('payment_method')
        Payment.objects.create(order=order, payment_method=payment_method, payment_status="Success")
        order.status = "Completed"
        order.save()
        return redirect('payment_success', order_id=order.id)
    return render(request, 'shop/register_payment.html', {'order': order})

#@login_required
def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/payment_success.html', {'order': order})
