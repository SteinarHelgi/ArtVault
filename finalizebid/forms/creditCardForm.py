from django import forms
from django.forms import ModelForm
from finalizebid.models import CreditCardModel

class CreditCardForm(ModelForm):
    class Meta:
        model = CreditCardModel
        fields = ['cardholder_name', 'card_number', 'card_cvv', 'card_expiration']
        widgets = {
            'cardholder_name': forms.TextInput(attrs={'class': 'form-control'}),
            'card_number': forms.TextInput(attrs={'class': 'form-control'}),
            'card_cvv': forms.TextInput(attrs={'class': 'form-control'}),
            'card_expiration': forms.TextInput(attrs={'class': 'form-control'}),
        }