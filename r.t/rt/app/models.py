# app/models.py (add this to your existing models)
from django.db import models

class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ('order-inquiry', 'Order Inquiry'),
        ('product-question', 'Product Question'),
        ('shipping-info', 'Shipping Information'),
        ('return-exchange', 'Return & Exchange'),
        ('wholesale', 'Wholesale Inquiry'),
        ('collaboration', 'Collaboration'),
        ('complaint', 'Complaint'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    order_number = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField()
    newsletter = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
    
    def __str__(self):
        return f"{self.name} - {self.get_subject_display()} - {self.created_at.strftime('%Y-%m-%d')}"