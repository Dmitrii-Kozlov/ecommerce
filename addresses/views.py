from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from billing.models import BillingProfile
from .forms import AddressForm
from .models import Address
# Create your views here.

def address_create_view(request):
    form = AddressForm(request.POST or None)
    content = {
        "form": form
    }
    next_ = request.GET.get('next')
    post_next_ = request.POST.get('next')
    redirect_path = next_ or post_next_ or None
    if form.is_valid():
        instance = form.save(commit=False)
        address_type = request.POST.get('address_type', 'shipping')
        instance.address_type = address_type
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            instance.billing_profile = billing_profile
            instance.save()
            request.session[address_type + "_address_id"] = instance.id
            print(address_type + "_address_id")
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('carts:checkout')
        else:
            print('Error')
            return redirect('carts:checkout')
    return redirect('carts:checkout')

def address_reuse_view(request):
    if request.user.is_authenticated:
        next_ = request.GET.get('next')
        post_next_ = request.POST.get('next')
        redirect_path = next_ or post_next_ or None
        if request.method == 'POST':
            print(request.POST)
            address_type = request.POST.get('address_type', 'shipping')
            shipping_address = request.POST.get('shipping_address', None)
            billing_profile, created = BillingProfile.objects.new_or_get(request)
            if shipping_address is not None:
                qs = Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
                if qs.exists():
                    request.session[address_type + "_address_id"] = shipping_address
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
                return redirect('carts:checkout')
    return redirect('carts:checkout')