from django.urls import path
from .views import ProductListView, product_list_view, ProductDetailView, product_detail_view
urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    # path('', product_list_view, name='list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='detail'),
    # path('<pk>/', product_detail_view, name='detail'),
]