from datetime import timedelta
from django.db import models
from django.utils import timezone

from user.models import BuyerProfileModel, SellerProfileModel

# Create your models here.


def default_end_date():
    return timezone.now().date() + timedelta(days=7)


class Artwork(models.Model):
    objects = models.Manager()

    seller = models.ForeignKey(
        SellerProfileModel, on_delete=models.CASCADE, related_name="artworks"
    )
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
    auction_start_date = models.DateField()
    auction_end_date = models.DateField()


class ArtworkImage(models.Model):
    objects = models.Manager()
    image = models.ImageField(upload_to="artworks/")
    artwork = models.ForeignKey(
        Artwork, on_delete=models.CASCADE, related_name="images"
    )


class Bid(models.Model):
    objects = models.Manager()
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    status = models.CharField(max_length=255)
    buyer = models.ForeignKey(BuyerProfileModel, on_delete=models.CASCADE)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name="bids")


class ArtmovementArtist(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    portrait = models.ImageField(upload_to="artmovements/portraits/")

    def __str__(self):
        return self.name


class Artmovement(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=255)
    period = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    artists = models.ManyToManyField(ArtmovementArtist, related_name="movements")

    def __str__(self):
        return self.name


class ArtmovementArtwork(models.Model):
    objects = models.Manager()
    artmovement = models.ForeignKey(Artmovement, on_delete=models.CASCADE, related_name="artworks")
    artmovement_artist = models.ForeignKey(ArtmovementArtist, on_delete=models.CASCADE, related_name="artworks")
    images = models.ImageField(upload_to="artworks/")
    title = models.CharField(max_length=255, null=True)
