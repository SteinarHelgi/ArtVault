from django.http import HttpResponse
from django.shortcuts import render
from .data import artworks


# Create your views here
def index(request):
    return render(request, "artvault/artvault.html", {"art": artworks})


def get_art_by_id(request, id):
    return HttpResponse(f"Hi there! {request.path},with ID {id}")
