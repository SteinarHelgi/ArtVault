from django import forms
from user.models import BuyerProfileModel


class BuyerProfileForm(forms.ModelForm):

    profile_image = forms.ImageField(
        required=False,
        error_messages={
            "required": "Please upload a profile image."
        },
        widget=forms.FileInput(attrs={
            'class': 'hidden-file-input',
            'onchange': 'previewBuyerProfileImage(event)'
        })
    )

    class Meta:
        model = BuyerProfileModel
        exclude = ('user', 'id', 'profile')

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'profile-input',
                'placeholder': 'Full Name'
            }),
        }

    def clean_profile_image(self):
        profile_image = self.cleaned_data.get("profile_image")

        if not profile_image:
            raise forms.ValidationError("Please upload a profile image.")

        return profile_image