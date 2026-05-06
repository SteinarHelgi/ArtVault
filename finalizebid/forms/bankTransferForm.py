from django import forms
from django.forms import ModelForm
from finalizebid.models import BankTransferModel

class BankTransferForm(ModelForm):
    class Meta:
        model = BankTransferModel
        fields = ['bank', 'hb', 'account']
        widgets = {
            'bank' : forms.TextInput(attrs={'class': 'form-control'}),
            'hb' : forms.TextInput(attrs={'class': 'form-control'}),
            'account' : forms.TextInput(attrs={'class': 'form-control'}),
        }
