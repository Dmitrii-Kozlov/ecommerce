from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from billing.models import BillingProfile
from .forms import AddressForm
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
        instance.address_type = request.POST.get('address_type', 'shipping')
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        if billing_profile is not None:
            instance.billing_profile = billing_profile
            instance.save()
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('carts:checkout')
        else:
            print('Error')
            return redirect('carts:checkout')
    return redirect('carts:checkout')