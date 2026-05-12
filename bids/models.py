from django.db import models
from django_countries.fields import CountryField

from artvault.models import Bid


# Create your models here.
class ShippingModel(models.Model):
    objects = models.Manager()
    PAYMENT_CHOICES = [
        ("card", "Credit Card"),
        ("bank", "Bank Transfer"),
        ("wire", "Wire Transfer"),
    ]
    bid = models.ForeignKey(
        Bid,
        on_delete=models.CASCADE,
        related_name="shipping_details",
        null=True,
        blank=True,
    )
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_CHOICES, blank=True, default=""
    )

    email = models.CharField(max_length=100)
    country = CountryField()
    national_id = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)


class CreditCardModel(models.Model):
    objects = models.Manager()
    shipping = models.OneToOneField(ShippingModel, on_delete=models.CASCADE)

    cardholder_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=20)
    card_cvv = models.CharField(max_length=20)
    card_expiration = models.CharField(max_length=20)


class BankTransferModel(models.Model):
    objects = models.Manager()
    shipping = models.OneToOneField(ShippingModel, on_delete=models.CASCADE)

    bank = models.CharField(max_length=4)
    hb = models.CharField(max_length=2)
    account = models.CharField(max_length=6)


class WireTransferModel(models.Model):
    objects = models.Manager()
    shipping = models.OneToOneField(ShippingModel, on_delete=models.CASCADE)

    sending_bank = models.CharField(max_length=100)
    routing_number = models.CharField(max_length=8)
    account_number = models.CharField(max_length=12)
