from django import forms
from django.core.validators import RegexValidator


numbers_only = RegexValidator(
    regex=r"^\d+$",
    message="Only numbers are allowed.",
)


class BankTransferForm(forms.Form):
    bank = forms.CharField(
        validators=[numbers_only],
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "0000",
        })
    )

    hb = forms.CharField(
        validators=[numbers_only],
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "00",
            "inputmmode": "numberic"
        })
    )

    account = forms.CharField(
        validators=[numbers_only],
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "000000",
        })
    )
