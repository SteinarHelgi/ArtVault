from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("browse_artwork/", views.browse_artwork, name="artvault-browse-artwork"),
    path(
        "artwork_details/<int:id>/",
        views.artwork_details,
        name="artvault-artwork-details",
    ),
]
