from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("browse_artwork/", views.browse_artwork, name="browse-artwork"),
    path(
        "artwork_details/<int:id>/",
        views.artwork_details,
        name="artwork-details",
    ),
    path("browse_artists/", views.browse_artists, name="browse-artists"),
    path("public_seller_profile_view/<int:id>/", views.public_seller_profile_view, name="public-seller-profile"),
    path("view_sellers/",views.view_sellers,name="view-sellers"),
    path("movements/",views.movements,name="movements"),
    path("artists/<slug:slug>/",views.movement_artists,name="movement-artist"),
    path("my_profile_seller/", views.my_profile_seller, name="my-profile-seller"),
    path("contact_us/", views.contact_us, name="contact-us"),
    path("common_questions/", views.common_questions, name="common-questions"),
    path("about_us/", views.about_us, name="about-us"),
]
