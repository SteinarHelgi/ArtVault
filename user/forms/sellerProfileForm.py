from django import forms
from django.forms import ModelForm
from user.models import SellerProfileModel
from user.models import Profile

class SellerProfileForm(ModelForm):
    class Meta:
        model = SellerProfileModel
        exclude = ('user', 'id', 'profile')
        widgets = {
            'seller_name': forms.TextInput(attrs={'placeholder': 'Full name'}),
            'street_name': forms.TextInput(attrs={'placeholder': 'Street name'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'zip_code': forms.TextInput(attrs={'placeholder': 'Postal code'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'hidden-file-input', }),
            'cover_photo': forms.ClearableFileInput(attrs={'class': 'hidden-file-input'}),
            'bio': forms.TextInput(attrs={'placeholder': 'About me...'}),
        }

