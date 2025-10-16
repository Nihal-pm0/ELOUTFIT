# contact/admin.py
from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_resolved']
    list_filter = ['subject', 'is_resolved', 'created_at', 'newsletter']
    search_fields = ['name', 'email', 'message', 'order_number']
    readonly_fields = ['created_at', 'ip_address']
    list_per_page = 20
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'subject', 'order_number')
        }),
        ('Message', {
            'fields': ('message', 'newsletter')
        }),
        ('Metadata', {
            'fields': ('created_at', 'ip_address', 'is_resolved'),
            'classes': ('collapse',)
        }),
    )

    