from django.contrib import admin
from .models import BillingProfile
# Register your models here.


@admin.register(BillingProfile)
class AdminBillingProfile(admin.ModelAdmin):
    list_display = ['user', 'email']