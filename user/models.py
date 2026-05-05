from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('individual', 'Individual'),
        ('gallery', 'Gallery'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(choices=ROLE_CHOICES, max_length=100)

    #buyer profile
    full_name = models.CharField(max_length=100)
    profile_image = models.TextField(max_length=9999)

    #seller profile
    seller_name = models.CharField(max_length=100)
    street_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    logo = models.TextField(max_length=9999)
    cover_photo = models.TextField(max_length=9999)
    bio = models.TextField(max_length=9999)


