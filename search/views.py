from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product

class SearchProductView(ListView):
    queryset = Product.objects.all()
    template_name = "search/view.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchProductView, self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.none()
