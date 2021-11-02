from django.shortcuts import render, redirect
from .models import Cart
from accounts.models import GuestEmail
from billing.models import BillingProfile
from products.models import Product
from orders.models import Order
from accounts.forms import LoginForm, GuestForm
from addresses.forms import AddressForm
from addresses.models import Address


def cart_home(request):
    cart_obj, is_new_obj = Cart.objects.get_or_create(request)
    return render(request, 'carts/home.html', {'cart': cart_obj})

def cart_update(request):
    # print(request.POST)
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            cart_obj, is_new_obj = Cart.objects.get_or_create(request)
        except Product.DoesNotExist:
            print("Message for user, product gone?")
            return redirect('carts:home')
        product_obj = Product.objects.get(id=product_id)
        if product_obj not in cart_obj.products.all():
            cart_obj.products.add(product_obj)
        else:
            cart_obj.products.remove(product_obj)
        request.session['cart_items'] = cart_obj.products.count()
    # return redirect('products:detail', product_obj.slug)
        return redirect('carts:home')


def checkout_home(request):
    cart_obj, is_new_obj = Cart.objects.get_or_create(request)
    order_obj = None
    if is_new_obj or cart_obj.products.count() == 0:
        redirect('carts:home')

    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)
    billing_profile, created = BillingProfile.objects.new_or_get(request)
    if billing_profile is not None:
        order_obj, created = Order.objects.get_or_new(billing_profile=billing_profile, cart_obj=cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if shipping_address_id or billing_address_id:
            order_obj.save()

    if request.method == 'POST':
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            request.session['cart_items'] = 0
            del request.session['cart_id']
            return redirect('/cart/success/')

    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
        'address_form': address_form,
    }
    return render(request, 'carts/checkout.html', context)


