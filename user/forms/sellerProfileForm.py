from django import forms
from django.forms import ModelForm
from user.models import SellerProfileModel

class SellerProfileForm(ModelForm):
    logo = forms.ImageField(
        required=False,
        error_messages={
            "required": "Please upload a logo."
        },
        widget=forms.FileInput(attrs={
            'class': 'hidden-file-input',
            'onchange': 'previewLogo(event)'
        })
    )

    cover_photo = forms.ImageField(
        required=False,
        error_messages={
            "required": "Please upload a cover photo."
        },
        widget=forms.FileInput(attrs={
            'class': 'hidden-file-input',
            'onchange': 'previewCover(event)'
        })
    )
    zip_code = forms.RegexField(regex=r'^\d{3}$',
        error_messages={
            "invalid": "Postal code must be exactly 3 numbers."
        },
        widget=forms.TextInput(attrs={
            'placeholder': 'Postal code'
        })
    )
    class Meta:
        model = SellerProfileModel
        exclude = ('user', 'id', 'profile')
        widgets = {
            'seller_name': forms.TextInput(attrs={'placeholder': 'Full name'}),
            'street_name': forms.TextInput(attrs={'placeholder': 'Street name'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'hidden-file-input', 'onchange': 'previewLogo(event)' }),
            'cover_photo': forms.ClearableFileInput(attrs={'class': 'hidden-file-input','onchange': 'previewCover(event)'}),
            'bio': forms.Textarea(attrs={'placeholder': 'About me...'}),
        }

    def clean_logo(self):
        logo = self.cleaned_data.get("logo")

        if not logo:
            raise forms.ValidationError("Please upload a logo.")

        return logo

    def clean_cover_photo(self):
        cover_photo = self.cleaned_data.get("cover_photo")

        if not cover_photo:
            raise forms.ValidationError("Please upload a cover photo.")

        return cover_photo

