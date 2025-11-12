from django.db import models
from django.conf import settings
from products.models import Product

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart ({self.user.username})"
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())
    
    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())
    
    @property
    def is_valid(self):
        """Check if all items in cart are available and in stock"""
        for item in self.items.all():
            if not item.product.available or item.quantity > item.product.stock:
                return False
        return True

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['cart', 'product']
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    @property
    def total_price(self):
        return self.product.price * self.quantity