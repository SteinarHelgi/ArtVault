from django.db import models

from artvault.models import Artwork, Bid
from user.models import BuyerProfileModel, SellerProfileModel


class Order(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.PROTECT, related_name="orders")
    buyer = models.ForeignKey(BuyerProfileModel, on_delete=models.PROTECT, related_name="orders")
    seller = models.ForeignKey(SellerProfileModel, on_delete=models.PROTECT, related_name="orders")
    bid = models.OneToOneField(Bid, on_delete=models.PROTECT, related_name="order")

    purchase_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.artwork.title} sold to {self.buyer}"
