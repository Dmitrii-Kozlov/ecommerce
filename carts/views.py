from django.shortcuts import render, redirect
from .models import Cart
from products.models import Product


def cart_home(request):
    cart_obj, is_new_obj = Cart.objects.get_or_create(request)
    return render(request, 'carts/view.html', {})

def cart_update(request):
    product_id = 1
    cart_obj, is_new_obj = Cart.objects.get_or_create(request)
    product_obj = Product.objects.get(id=product_id)
    if product_obj not in cart_obj.products.all():
        cart_obj.products.add(product_obj)
    else:
        cart_obj.products.remove(product_obj)
    return redirect('carts:home')

