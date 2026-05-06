from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('individual_seller', 'Individual Seller'),
        ('gallery', 'Gallery'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'signup-input'}))

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'signup-input', 'placeholder': 'Username...'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'signup-input', 'placeholder': 'Password...'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'signup-input', 'placeholder': 'Confirm Password...'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']

