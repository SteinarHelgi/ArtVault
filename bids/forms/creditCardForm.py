from django import forms
from django.forms import ModelForm
from bids.models import CreditCardModel
from django.core.validators import RegexValidator

expiry_validator = RegexValidator(
    regex=r"^(0[1-9]|1[0-2])\/\d{2}$",
    message="Enter expiry date as MM/YY"
)
class CreditCardForm(ModelForm):
    card_expiration = forms.CharField(validators=[expiry_validator],widget=forms.TextInput(attrs={"class": "card-expiration-input","placeholder": "MM/YY", "maxlength": "5", "autocomplete": "off"}))

    class Meta:
        model = CreditCardModel
        fields = ['cardholder_name', 'card_number', 'card_cvv', 'card_expiration']
        widgets = {
            'cardholder_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'card_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0000-0000-0000-0000'}),
            'card_cvv': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000'}),
        }
