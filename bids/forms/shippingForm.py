from django import forms
from django.forms import ModelForm
from bids.models import ShippingModel
from django_countries.fields import CountryField

class ShippingForm(ModelForm):

    country = CountryField(blank_label='Country/Region').formfield()

    class Meta:
        model = ShippingModel
        fields = ['email', 'country', 'national_id', 'street_name', 'city', 'zip_code']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'National ID'}),
            'street_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Name'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
        }
