from django.urls import path
from .views import (
    cart_home,
    cart_update)

app_name = 'products'

urlpatterns = [
    path('', cart_home, name='home'),
    path('update/', cart_update, name='update'),
]