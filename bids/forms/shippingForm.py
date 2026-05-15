from django import forms
from django.core.validators import RegexValidator
from django_countries.fields import CountryField


national_id_validator = RegexValidator(
    regex=r"^\d{10}$",
    message="Enter a valid national ID.",
)

zip_code_validator = RegexValidator(
    regex=r"^\d+$",
    message="Postal code must contain only numbers.",
)


class ShippingForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Email",
        })
    )

    country = CountryField(blank_label="Country/Region").formfield(
        widget=forms.Select(attrs={
            "class": "form-control",
        })
    )

    national_id = forms.CharField(
        validators=[national_id_validator],
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "National ID",
        })
    )

    street_name = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Street Name",
        })
    )

    city = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "City",
        })
    )

    zip_code = forms.CharField(
        validators=[zip_code_validator],
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Postal Code",
        })
    )
