from django.db import models

from user.models import SellerProfileModel

# Create your models here.


class Artwork(models.Model):
    objects = models.Manager()
    seller = models.ForeignKey(SellerProfileModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    medium = models.CharField(max_length=255)
    edition = models.CharField(max_length=255)
    dimensions = models.CharField(max_length=255)
    sold = models.BooleanField()
    history = models.CharField(max_length=4096)
    artist_name = models.CharField(max_length=255)
    date = models.DateField()
    starting_price = models.CharField(max_length=255)
    art_movement = models.CharField(max_length=255)


class ArtWorkImage(models.Model):
    image_path = models.CharField(max_length=255)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
