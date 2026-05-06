from django.urls import path
from . import views

urlpatterns = [
    path("shipping/<int:bid_id>/", views.shipping, name="shipping"),
    path("shipping/edit/<int:shipping_id>/", views.shipping_edit, name="shipping_edit"),
    path("payment-method/<int:shipping_id>/", views.payment_method, name="payment_method"),
    path("card-payment/<int:shipping_id>/", views.credit_card_payment, name="credit_card_payment"),
    path("bank-payment/<int:shipping_id>/", views.bank_transfer_payment, name="bank_transfer_payment"),
    path("wire-payment/<int:shipping_id>/", views.wire_transfer_payment, name="wire_transfer_payment"),
    path("overview/<int:shipping_id>/", views.checkout_overview, name="checkout_overview"),
    path("my_bids/", views.my_bids, name="my_bids"),
]
