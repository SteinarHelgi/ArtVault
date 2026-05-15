from django.urls import path
from . import views

urlpatterns = [
    path("shipping/<int:bid_id>/", views.shipping, name="shipping"),
    path("payment-method/<int:bid_id>/", views.payment_method, name="payment_method"),
    path("card-payment/<int:bid_id>/", views.credit_card_payment, name="credit_card_payment"),
    path("bank-payment/<int:bid_id>/", views.bank_transfer_payment, name="bank_transfer_payment"),
    path("wire-payment/<int:bid_id>/", views.wire_transfer_payment, name="wire_transfer_payment"),
    path("overview/<int:bid_id>/", views.checkout_overview, name="checkout_overview"),
    path("my_bids/", views.my_bids, name="my_bids"),
    path("artwork/<int:artwork_id>/bid/make",views.make_bid,name="make_bid"),
    path("artwork/<int:artwork_id>/bid/submit", views.submit_bid, name="submit_bid"),
]
