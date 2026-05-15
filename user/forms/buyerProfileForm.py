from django import forms
from django.forms import ModelForm
from user.models import BuyerProfileModel

class BuyerProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(required=True, widget= forms.FileInput(attrs={'class': 'hidden-file-input','onchange': 'previewBuyerProfileImage(event)'}))

    class Meta:
        model = BuyerProfileModel
        exclude = ('user', 'id', 'profile')
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'profile-input', 'placeholder': 'Full Name'}),
        }