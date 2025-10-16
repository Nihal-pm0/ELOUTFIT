from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

# payments/urls.py
urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('create-razorpay-order/', views.create_razorpay_order, name='create_razorpay_order'),
    path('create-cod-order/', views.create_cod_order, name='create_cod_order'),
    path('payment/verify/', views.payment_verify, name='payment_verify'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/failed/', views.payment_failed, name='payment_failed'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
