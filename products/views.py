from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Product

class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/product_list.html"

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(ProductListView, self).get_context_data(object_list=None, **kwargs)
    #     return context

def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/product_list.html", context)


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    # template_name = "products/product_detail.html"

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(ProductListView, self).get_context_data(object_list=None, **kwargs)
    #     return context


def product_detail_view(request, pk):
    # object = Product.objects.get(pk=pk)
    object = get_object_or_404(Product, pk=pk)
    context = {
        'object': object
    }
    return render(request, "products/product_detail.html", context)