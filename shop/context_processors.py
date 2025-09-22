from .cart import Cart

def cart_item_count(request):
    try:
        cart = Cart(request)
        return {'cart_item_count': len(cart)}
    except Exception:
        return {'cart_item_count': 0}
