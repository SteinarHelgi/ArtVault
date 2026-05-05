from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('individual_seller', 'Individual Seller'),
        ('gallery', 'Gallery'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']

