from django import forms
from django.forms import ModelForm
from user.models import BuyerProfileModel

class BuyerProfileForm(forms.ModelForm):
    class Meta:
        model = BuyerProfileModel
        exclude = ('user', 'id', 'profile')
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'profile-input', 'placeholder': 'Full Name'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'hidden-file-input'}),
        }