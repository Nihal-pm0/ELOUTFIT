from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem
from products.models import Product
@login_required(login_url='/account/login/')  # Specify login URL
def cart_detail(request):
    try:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return render(request, 'cart/cart_detail.html', {'cart': cart})
    except Exception as e:
        messages.error(request, "There was an error accessing your cart.")
        return redirect('product_list')

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if product already in cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, 
        product=product
    )
    
    if not created:
        # If item already exists, increase quantity
        cart_item.quantity += 1
    else:
        # If new item, set quantity to 1
        cart_item.quantity = 1
    
    cart_item.save()
    messages.success(request, f'{product.name} added to cart!')
    
    # Redirect back to product page or cart
    if 'next' in request.GET:
        return redirect(request.GET['next'])
    return redirect('cart:cart_detail')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} removed from cart!')
    return redirect('cart:cart_detail')

@login_required
def update_cart(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        
        # Stock validation
        if quantity > cart_item.product.stock:
            messages.warning(request, f'Only {cart_item.product.stock} items available for {cart_item.product.name}')
            quantity = cart_item.product.stock
        
        if quantity < 1:
            cart_item.delete()
            messages.success(request, 'Item removed from cart')
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully')
        
        return redirect('cart:cart_detail')

@login_required
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    messages.success(request, 'Cart cleared successfully!')
    return redirect('cart:cart_detail')