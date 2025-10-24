from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('order.urls')),
    path('account/', include('account.urls')),
    path('payments/', include('payments.urls')),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
    path('search/', views.search_products, name='search'),
    path('error-tests/', views.error_test_dashboard, name='error_test_dashboard'),
    path('error-tests/404/', views.test_404, name='test_404'),
    path('error-tests/500/', views.test_500, name='test_500'),
    path('error-tests/403/', views.test_403, name='test_403'),
    path('error-tests/400/', views.test_400, name='test_400'),
    
    # Real error triggers
    path('error-tests/real-404/', lambda request: render(request, 'nonexistent.html')),
    path('error-tests/real-403/', lambda request: HttpResponse('Forbidden', status=403)),
 
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
