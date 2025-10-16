import razorpay
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from order.models import Order, OrderItem

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
from cart.models import Cart  # Import your Cart model

@login_required
def checkout(request):
    # Get the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if cart is empty
    if not cart.items.exists():
        return redirect('cart:cart_detail')  # Redirect to cart if empty
    
    if request.method == 'POST':
        # Pass data to payment options (NO ORDER CREATED YET)
        context = {
            'customer_data': {
                'full_name': request.POST.get('full_name'),
                'email': request.user.email,
                'phone': request.POST.get('phone'),
                'address': request.POST.get('address'),
            },
            'total_amount': cart.total_price,  # This will work now
        }
        return render(request, 'payments/payment_options.html', context)
    
    # GET request - show checkout form with cart data
    return render(request, 'payments/checkout.html', {'cart': cart})


@login_required
def create_razorpay_order(request):
    # ONLY creates order when user clicks Razorpay payment
    pass

@login_required  
def create_cod_order(request):
    # ONLY creates order when user clicks COD
    pass

@login_required
def payment_success(request):
    return render(request, 'payments/success.html')

@login_required
def payment_failed(request):
    return render(request, 'payments/failed.html')
@login_required
def payment_verify(request):
    if request.method == "POST":
        try:
            razorpay_payment_id = request.POST.get('razorpay_payment_id')
            razorpay_order_id = request.POST.get('razorpay_order_id')
            razorpay_signature = request.POST.get('razorpay_signature')
            
            # Verify payment signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            
            client.utility.verify_payment_signature(params_dict)
            
            # Update order status
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
            order.razorpay_payment_id = razorpay_payment_id
            order.razorpay_signature = razorpay_signature
            order.status = 'paid'
            order.save()
            
            # ✅ CLEAR CART AFTER SUCCESSFUL PAYMENT
            from cart.models import Cart
            cart = Cart.objects.get(user=order.user)
            cart.items.all().delete()  # Delete all cart items
            
            messages.success(request, "Payment successful! Your order has been confirmed.")
            return redirect('payment_success')
            
        except Exception as e:
            messages.error(request, "Payment verification failed.")
            return redirect('payment_failed')
    
    return redirect('checkout')


@login_required
def create_razorpay_order(request):
    if request.method == 'POST':
        # Get cart
        from cart.models import Cart
        cart = get_object_or_404(Cart, user=request.user)
        
        total_amount = float(request.POST.get('total_amount'))
        amount_in_paise = int(total_amount * 100)
        
        # Create order in database
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            status='pending'
        )
        
        # Add order items from cart
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
        
        # Create Razorpay order
        razorpay_order = client.order.create({
            'amount': amount_in_paise,
            'currency': 'INR',
            'receipt': order.order_number,
            'payment_capture': 1
        })
        
        order.razorpay_order_id = razorpay_order['id']
        order.save()
        
        context = {
            'order': order,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'amount': amount_in_paise,
        }
        return render(request, 'payments/payment.html', context)
    
    return redirect('checkout')

@login_required
def create_cod_order(request):
    if request.method == 'POST':
        # Get cart
        from cart.models import Cart
        cart = get_object_or_404(Cart, user=request.user)
        
        # Create Cash on Delivery order
        order = Order.objects.create(
            user=request.user,
            total_amount=request.POST.get('total_amount'),
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            status='processing'  # COD orders are processing
        )
        
        # Add order items from cart
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
        
        # ✅ CLEAR CART AFTER COD ORDER
        cart.items.all().delete()  # Delete all cart items
        
        messages.success(request, "COD order placed successfully!")
        return redirect('payment_success')
    
    return redirect('checkout')
def payment_success(request):
    return render(request, 'payments/success.html')