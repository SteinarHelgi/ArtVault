from django import forms
from django.forms import ModelForm
from user.models import BuyerProfileModel, SellerProfileModel


class BuyerAccountSettingsForm(ModelForm):
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label="New password"
    )

    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label="Confirm password"
    )

    profile_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'hidden-file-input', 'onchange': 'previewBuyerProfileImage(event)'}))

    class Meta:
        model = BuyerProfileModel
        fields = [
            "full_name",
            "profile_image",
        ]

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("new_password")
        confirm = cleaned_data.get("confirm_password")

        if password or confirm:
            if password != confirm:
                raise forms.ValidationError("Passwords do not match")

        return cleaned_data


class IndividualSellerAccountSettingsForm(ModelForm):
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label="New password"
    )

    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label="Confirm password"
    )
    logo = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={'class': 'hidden-file-input', 'onchange': 'previewLogo(event)'}))
    cover_photo = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={'class': 'hidden-file-input', 'onchange': 'previewCover(event)'}))

    class Meta:
        model = SellerProfileModel
        fields = [
            "seller_name",
            "logo",
            "cover_photo",
            "bio"
        ]

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("new_password")
        confirm = cleaned_data.get("confirm_password")

        if password or confirm:
            if password != confirm:
                raise forms.ValidationError("Passwords do not match")

        return cleaned_data


class GalleryAccountSettingsForm(ModelForm):
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label="New password"
    )

    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label="Confirm password"
    )
    logo = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={'class': 'hidden-file-input', 'onchange': 'previewLogo(event)'}))
    cover_photo = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={'class': 'hidden-file-input', 'onchange': 'previewCover(event)'}))

    class Meta:
        model = SellerProfileModel
        fields = [
            "seller_name",
            "logo",
            "cover_photo",
            "bio",
            "street_name",
            "city",
            "zip_code",
        ]

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("new_password")
        confirm = cleaned_data.get("confirm_password")

        if password or confirm:
            if password != confirm:
                raise forms.ValidationError("Passwords do not match")

        return cleaned_data