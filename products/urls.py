from django.urls import path
from .views import (
    ProductListView,
    product_list_view,
    ProductDetailView,
    ProductDetailSlugView,
    product_detail_view,
    ProductFeaturedListView,
    ProductFeaturedDetailView
)
urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    # path('', product_list_view, name='list'),
    # path('<int:pk>/', ProductDetailView.as_view(), name='detail'),
    path('<slug:slug>/', ProductDetailSlugView.as_view(), name='detail'),
    # path('<pk>/', product_detail_view, name='detail'),
    path('featured/', ProductFeaturedListView.as_view(), name='featured_list'),
    path('featured/<int:pk>/', ProductFeaturedDetailView.as_view(), name='featured_detail'),
]