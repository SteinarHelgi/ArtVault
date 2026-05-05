from django import forms
from django.forms import ModelForm
from user.models import Profile


class BuyerProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'profile_image']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.TextInput(attrs={'class': 'form-control'}),
        }