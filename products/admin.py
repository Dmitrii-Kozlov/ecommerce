from django.contrib import admin

# Register your models here.

from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # class Meta:
    #     model = Product
    list_display = ['title', 'slug']
    # prepopulated_fields = {'slug': ['title']}