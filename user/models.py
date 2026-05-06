from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    ROLE_CHOICES = [
        ("buyer", "Buyer"),
        ("individual", "Individual"),
        ("gallery", "Gallery"),
    ]

    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(choices=ROLE_CHOICES, max_length=100)



class BuyerProfileModel(models.Model):
    # buyer profile
    objects = models.Manager()
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name="buyer_profile",
    )
    full_name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='profile_images/')


class SellerProfileModel(models.Model):
    # seller profile
    objects = models.Manager()
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name="seller_profile",
    )
    seller_name = models.CharField(max_length=100)
    street_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    logo =  models.ImageField(upload_to='logos/')
    cover_photo =  models.ImageField(upload_to='cover_photos/')
    bio = models.TextField(max_length=9999)
