from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Product
from carts.models import Cart


class ProductFeaturedListView(ListView):
    def get_queryset(self):
        qs = Product.objects.all().featured()
        return qs

class ProductFeaturedDetailView(DetailView):
    queryset = Product.objects.features()
    template_name = "products/product_featured_detail.html"

    # def get_queryset(self):
    #     qs = Product.objects.featured()
    #     return qs


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/product_list.html"

    def get_context_data(self, **kwargs):
        cart_obj, is_new_obj = Cart.objects.get_or_create(self.request)
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['cart'] = cart_obj
        return context
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(ProductListView, self).get_context_data(object_list=None, **kwargs)
    #     return context

def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/product_list.html", context)

class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        cart_obj, is_new_obj = Cart.objects.get_or_create(self.request)
        context = super(ProductDetailSlugView, self).get_context_data(**kwargs)
        context['cart'] = cart_obj
        return context
    def get_object(self, queryset=None, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Does not exist...")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Unknown thing...")
        return instance

class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    # template_name = "products/product_detail.html"

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(ProductListView, self).get_context_data(object_list=None, **kwargs)
    #     return context

    def get_object(self, queryset=None, **kwargs):
        request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404('Product does not exist.')
        return instance


def product_detail_view(request, pk):
    # object = Product.objects.get(pk=pk)
    object = get_object_or_404(Product, pk=pk)
    instance = Product.objects.get_by_id(pk)
    print(instance)
    context = {
        'object': object
    }
    return render(request, "products/product_detail.html", context)