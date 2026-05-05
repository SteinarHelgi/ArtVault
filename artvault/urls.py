from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="artvault-index"),

    path("artwork_details/<int:id>", views.artwork_details, name="artwork-details"),
]
