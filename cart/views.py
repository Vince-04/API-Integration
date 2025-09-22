from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .cart import Cart
from shop.models import Product


def cart_summary(request):
    cart = Cart(request)
    return render(request, "cart/cart_summary.html", {"cart": cart})


def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=quantity)
        return JsonResponse({'qty': len(cart)})


def cart_delete(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect("cart:cart_summary")


def cart_update(request, product_id):
    cart = Cart(request)
    quantity = int(request.POST.get("quantity", 1))
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=quantity, update_quantity=True)
    return redirect("cart:cart_summary")


def checkout(request):
    cart = Cart(request)
    return render(request, 'cart/cart_checkout.html', {'cart': cart})
