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

    @property
    def formatted_amount(self):
        return f"{self.amount:,}".replace(",", ".")
