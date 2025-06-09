from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from cart.cart import Cart
from shop.models import Product


# Create your views here.

@require_POST
def add_to_cart(request, product_id):
    try:
        cart = Cart(request)
        product = get_object_or_404(Product, pk=product_id)
        cart.add(product)
        context = {
            'item_count':len(cart),
            'total_price':cart.get_total_price()
        }
        return JsonResponse(context)
    except:
        return JsonResponse({'error':'Something went wrong'})
