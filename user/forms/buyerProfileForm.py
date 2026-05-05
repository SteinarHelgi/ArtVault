from django import forms
from django.forms import ModelForm
from user.models import BuyerProfileModel

class BuyerProfileForm(forms.ModelForm):
    class Meta:
        model = BuyerProfileModel
        exclude = ('user', 'id')
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.TextInput(attrs={'class': 'form-control'}),
        }