from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone', 'address']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter your shipping address'
            }),
        }
        labels = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'address': 'Shipping Address',
        }
    
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if len(full_name.strip()) < 2:
            raise forms.ValidationError("Please enter a valid full name.")
        return full_name
    
    def clean_address(self):
        address = self.cleaned_data.get('address')
        if len(address.strip()) < 10:
            raise forms.ValidationError("Please enter a complete shipping address.")
        return address