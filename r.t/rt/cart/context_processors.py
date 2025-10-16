from .models import Cart

def cart_context(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return {
            'cart': cart,
            'cart_items_count': cart.items.count()
        }
    return {
        'cart': None,
        'cart_items_count': 0
    }