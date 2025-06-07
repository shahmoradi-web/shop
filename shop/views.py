from django.shortcuts import render, get_object_or_404
from .models import *

# Create your views here.

def product_list(request, category_slug = None):
    category = None
    products = Product.objects.all()
    categories = Category.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'products': products,
        'categories': categories,

    }
    return render(request, 'shop/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    context = {
        'product': product,
    }
    return render(request, 'shop/detail.html', context)