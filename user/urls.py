from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from . import views


urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", LoginView.as_view(template_name="user/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("buyer-profile/", views.buyer_profile, name="buyer_profile"),
    path("seller-profile/", views.seller_profile, name="seller_profile"),
    path("my_bids/", views.my_bids, name="my_bids"),
    path("finalize-bid/<int:bid_id>", views.finalize_bid, name="finalize-bid"),
    path("account_settings/", views.account_settings, name="account-settings"),
]
