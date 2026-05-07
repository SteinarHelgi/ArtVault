from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", LoginView.as_view(template_name="user/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("buyer-setup/", views.buyer_setup, name="buyer_setup"),
    path("seller-setup/", views.seller_setup, name="seller_setup"),
    path("my_profile_seller/", views.my_profile_seller, name="my_profile_seller"),
    path("account_settings/", views.account_settings, name="account-settings"),
]
