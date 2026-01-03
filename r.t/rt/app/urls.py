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
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
