from django.urls import path
from . import views

urlpatterns = [
    path("add_listing/", views.add_listing_view, name="add_listing"),
    path("my_listing/<int:id>", views.my_listing_view, name="my-listing"),
]
