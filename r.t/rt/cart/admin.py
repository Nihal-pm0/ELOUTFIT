from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_quantity', 'total_price', 'created_at']
    list_select_related = ['user']
    inlines = [CartItemInline]
    
    def total_quantity(self, obj):
        return obj.total_quantity
    total_quantity.short_description = 'Total Items'
    
    def total_price(self, obj):
        return f"${obj.total_price}"
    total_price.short_description = 'Total Price'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'cart', 'quantity', 'total_price', 'added_at']
    list_select_related = ['product', 'cart__user']
    
    def total_price(self, obj):
        return f"${obj.total_price}"
    total_price.short_description = 'Total Price'