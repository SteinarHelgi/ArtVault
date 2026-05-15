from django import forms
from django.core.validators import RegexValidator


card_number_validator = RegexValidator(
    regex=r"^\d{16}$",
    message="Enter a 16 digit card number.",
)

cvv_validator = RegexValidator(
    regex=r"^\d{3}$",
    message="Enter a 3 digit CVV.",
)

expiry_validator = RegexValidator(
    regex=r"^(0[1-9]|1[0-2])\/\d{2}$",
    message="Enter expiry date as MM/YY",
)


class CreditCardForm(forms.Form):
    cardholder_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Full Name",
            }
        )
    )

    card_number = forms.CharField(
        validators=[card_number_validator],
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "0000000000000000",
            }
        ),
    )

    card_cvv = forms.CharField(
        validators=[cvv_validator],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "000",
                "maxlength": "3",
                "autocomplete": "off",
                "inputmode": "numeric",
                "pattern": "[0-9]*",
            }
        ),
    )

    card_expiration = forms.CharField(
        validators=[expiry_validator],
        widget=forms.TextInput(
            attrs={
                "class": "card-expiration-input",
                "placeholder": "MM/YY",
                "maxlength": "5",
                "autocomplete": "off",
            }
        ),
    )
