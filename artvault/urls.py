from django.urls import path
from . import views

print("test 1")
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
]
