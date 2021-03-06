"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic import TemplateView

from accounts.views import LoginView, guest_register_view, RegisterView
from addresses.views import address_create_view, address_reuse_view
from carts.views import cart_detail_api_view
from .views import home, about, contact

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/cart/', cart_detail_api_view, name='cart-api'),
    path('cart/', include('carts.urls', namespace='carts')),
    path('address/create/', address_create_view, name='address_create'),
    path('address/reuse/', address_reuse_view, name='address_reuse'),
    path('register/guest', guest_register_view, name='guest_register'),
    path('register/', RegisterView.as_view(), name='register'),
    path('bootstrap/', TemplateView.as_view(template_name='bootstrap/example.html'), name='bootstrap'),
    path('products/', include('products.urls', namespace='products')),
    path('search/', include('search.urls', namespace='search')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)