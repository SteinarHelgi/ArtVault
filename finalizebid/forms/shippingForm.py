from django import forms
from django.forms import ModelForm
from finalizebid.models import ShippingModel

class ShippingForm(ModelForm):
    class Meta:
        model = ShippingModel
        fields = ['email', 'country', 'national_id', 'street_name', 'city', 'zip_code']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control'}),
            'street_name': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
        }