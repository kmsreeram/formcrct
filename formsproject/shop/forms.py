from django import forms
from .models import Products

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = "__all__"

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter the name of the product"}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Enter the price of the product"}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Enter the description of the product"}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Enter the stock quantity"}),
        }
