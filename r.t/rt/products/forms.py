from django import forms
from .models import ProductReview

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=ProductReview.RATING_CHOICES),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Review title'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your review here...'}),
        }
    
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating not in [1, 2, 3, 4, 5]:
            raise forms.ValidationError('Please select a valid rating.')
        return rating