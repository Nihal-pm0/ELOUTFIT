from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('clear/', views.clear_cart, name='clear_cart'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
