from django import forms
from django.forms import ModelForm
from bids.models import BankTransferModel

class BankTransferForm(ModelForm):
    class Meta:
        model = BankTransferModel
        fields = ['bank', 'hb', 'account']
        widgets = {
            'bank' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000'}),
            'hb' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00'}),
            'account' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000000'}),
        }
