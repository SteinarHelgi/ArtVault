from django.urls import path
from . import views

urlpatterns = [
    path("shipping/<int:bid_id>/", views.shipping, name="shipping"),
    path("payment-method/<int:bid_id>/", views.payment_method, name="payment-method"),
    path("card-payment/<int:bid_id>/", views.credit_card_payment, name="credit-card-payment"),
    path("bank-payment/<int:bid_id>/", views.bank_transfer_payment, name="bank-transfer-payment"),
    path("wire-payment/<int:bid_id>/", views.wire_transfer_payment, name="wire-transfer-payment"),
    path("overview/<int:bid_id>/", views.checkout_overview, name="checkout-overview"),
    path("my_bids/", views.my_bids, name="my-bids"),
    path("artwork/<int:artwork_id>/bid/make",views.make_bid,name="make-bid"),
    path("artwork/<int:artwork_id>/bid/submit", views.submit_bid, name="submit-bid"),
]
