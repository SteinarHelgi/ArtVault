from django import forms
from django.forms import ModelForm
from bids.models import CreditCardModel

class CreditCardForm(ModelForm):
    class Meta:
        model = CreditCardModel
        fields = ['cardholder_name', 'card_number', 'card_cvv', 'card_expiration']
        widgets = {
            'cardholder_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'card_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0000-0000-0000-0000'}),
            'card_cvv': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000'}),
            'card_expiration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY'}),
        }
