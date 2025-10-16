from pyexpat.errors import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Category 
import cart


def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Handle sorting
    sort = request.GET.get('sort', 'newest')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    else:  # newest (using id since no created field)
        products = products.order_by('-id')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'categories': categories,
        'page_obj': page_obj,
        'products': page_obj,
        'sort': sort,
    }
    return render(request, 'products/product_list.html', context)
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    related_products = Product.objects.filter(
        category=product.category, 
        available=True
    ).exclude(id=product.id)[:4]
    
    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products
    })

def single_product_view(request, slug):
    """Dedicated single product viewing page with enhanced features"""
    product = get_object_or_404(Product, slug=slug, available=True)
    
    # Get related products
    related_products = Product.objects.filter(
        category=product.category, 
        available=True
    ).exclude(id=product.id)[:4]
    
    # Handle Add to Cart
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            size = request.POST.get('size', '')
            color = request.POST.get('color', '')
            
            # Initialize cart
            cart = cart(request)
            cart.add(
                product=product,
                quantity=quantity,
                size=size,
                color=color
            )
            
            messages.success(request, f'✅ "{product.name}" added to cart!')
            return redirect('single_product_view', slug=product.slug)
            
        except Exception as e:
            messages.error(request, f'Error adding to cart: {str(e)}')
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/single_product_view.html', context)