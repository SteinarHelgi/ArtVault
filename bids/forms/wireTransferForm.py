from django import forms
from django.core.validators import RegexValidator


numbers_only = RegexValidator(
    regex=r"^\d+$",
    message="Only numbers are allowed.",
)


class WireTransferForm(forms.Form):
    sending_bank = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Name",
        })
    )

    routing_number = forms.CharField(
        validators=[numbers_only],
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "00000000",
        })
    )

    account_number = forms.CharField(
        validators=[numbers_only],
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "000000000000",
        })
    )
