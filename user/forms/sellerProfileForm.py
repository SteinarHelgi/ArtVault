from django import forms
from django.forms import ModelForm
from user.models import SellerProfileModel
from user.models import Profile

class SellerProfileForm(ModelForm):
    class Meta:
        model = SellerProfileModel
        exclude = ('user', 'id')
        widgets = {
            'seller_name': forms.TextInput(attrs={'class': 'form-control'}),
            'street_name': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.TextInput(attrs={'class': 'form-control'}),
            'cover_photo': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.TextInput(attrs={'class': 'form-control'}),
        }

