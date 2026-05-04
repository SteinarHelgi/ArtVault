from django.urls import path
from . import views

urlpatterns = [
    path('artwork_details/<int:id>', views.artwork_details, name='artwork-details'),
    path("", views.index, name="artvault-index"),
    path("steinar_test/", views.steinar_test, name="artvault-steinar_test"),
    path("<int:id>", views.get_art_by_id, name="artvault-index"),
]
