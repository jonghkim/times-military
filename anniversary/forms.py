from django import forms
from .models import restaurant, choice

class PostForm(forms.ModelForm):
    class Meta:
        model = restaurant
        fields = ('name', 'desc', 'phonenumber', 'url', 'restaurant_type',)
