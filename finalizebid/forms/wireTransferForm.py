from django import forms
from django.forms import ModelForm
from finalizebid.models import WireTransferModel

class WireTransferForm(ModelForm):
    class Meta:
        model = WireTransferModel
        fields = ['sending_bank', 'routing_number', 'account_number']
        widgets = {
            'sending_bank': forms.TextInput(attrs={'class': 'form-control'}),
            'routing_number': forms.TextInput(attrs={'class': 'form-control'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
    