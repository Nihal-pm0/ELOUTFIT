# app/forms.py (add this to your existing forms)
from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    SUBJECT_CHOICES = [
        ('', 'Select a subject'),
        ('order-inquiry', 'Order Inquiry'),
        ('product-question', 'Product Question'),
        ('shipping-info', 'Shipping Information'),
        ('return-exchange', 'Return & Exchange'),
        ('wholesale', 'Wholesale Inquiry'),
        ('collaboration', 'Collaboration'),
        ('complaint', 'Complaint'),
        ('other', 'Other'),
    ]
    
    subject = forms.ChoiceField(
        choices=SUBJECT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    order_number = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'If related to an order'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Please describe your inquiry in detail...',
            'minlength': '20'
        })
    )
    newsletter = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'order_number', 'message', 'newsletter']
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message.strip()) < 20:
            raise forms.ValidationError("Message must be at least 20 characters long.")
        return message