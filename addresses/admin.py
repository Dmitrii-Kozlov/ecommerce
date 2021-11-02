from django.contrib import admin
from .models import Address
# Register your models here.

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['billing_profile', 'address_type', 'address_line_1', 'country', 'state', 'city']