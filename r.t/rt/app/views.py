from django.shortcuts import render
from products.models import Product, Category
from django.db.models import Q

def home(request):
    # Get products for featured section
    featured_products = Product.objects.filter(available=True)[:8]
    
    # Get new arrivals
    new_arrivals = Product.objects.filter(available=True).order_by('-id')[:4]
    
    # Get all categories
    categories = Category.objects.all()
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'new_arrivals': new_arrivals,
    }
    return render(request, 'home.html', context)

def search(request):
    query = request.GET.get('q', '')
    categories = Category.objects.all()
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query),
            available=True
        )
    else:
        products = Product.objects.filter(available=True)
    
    context = {
        'products': products,
        'query': query,
        'categories': categories,
    }
    return render(request, 'products/search_results.html', context)

# app/views.py (add this to your existing views)
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView
from .forms import ContactForm
from .models import ContactMessage
import logging

logger = logging.getLogger(__name__)

class ContactView(TemplateView):
    template_name = 'contact.html'
    
    def get(self, request, *args, **kwargs):
        form = ContactForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            
            # Save to database
            contact_message = form.save(commit=False)
            contact_message.ip_address = ip
            contact_message.save()
            
            # Send email notification
            try:
                self.send_email_notification(contact_message)
            except Exception as e:
                logger.error(f"Failed to send email notification: {e}")
            
            messages.success(request, 'Thank you for your message! We will get back to you within 24 hours.')
            return redirect('contact')
        
        return render(request, self.template_name, {'form': form})
    
    def send_email_notification(self, contact_message):
        subject = f"New Contact Message: {contact_message.get_subject_display()}"
        message = f"""
        New contact form submission:
        
        Name: {contact_message.name}
        Email: {contact_message.email}
        Subject: {contact_message.get_subject_display()}
        Order Number: {contact_message.order_number or 'N/A'}
        
        Message:
        {contact_message.message}
        
        Received at: {contact_message.created_at}
        IP Address: {contact_message.ip_address}
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            ['revibe.threadss@gmail.com'],  # Your official email
            fail_silently=False,
        )

def contact_success(request):
    return render(request, 'contact_success.html')
# app/views.py
from django.shortcuts import render
from django.db.models import Q
from products.models import Product  # Adjust based on your app structure

def search_products(request):
    query = request.GET.get('q', '').strip()
    
    # If query is empty, show all products or recent products
    if not query:
        products = Product.objects.filter(available=True).order_by('-created_at')[:12]
    else:
        # Search for any product that contains the query (even single letters)
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).filter(available=True)
    
    return render(request, 'search_results.html', {
        'products': products,
        'query': query,
        'results_count': products.count()
    })


from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_GET

# Your existing views...

@require_GET
def error_test_dashboard(request):
    """Public error testing dashboard"""
    return render(request, 'error_test_dashboard.html')

@require_GET
def test_404(request):
    """Test 404 page"""
    return render(request, '404.html', status=404)

@require_GET
def test_500(request):
    """Test 500 page"""
    return render(request, '500.html', status=500)

@require_GET
def test_403(request):
    """Test 403 page"""
    return render(request, '403.html', status=403)

@require_GET
def test_400(request):
    """Test 400 page"""
    return render(request, '400.html', status=400)