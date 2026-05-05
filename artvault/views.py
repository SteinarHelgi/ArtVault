from django.http import HttpResponse
from django.shortcuts import render
from .data import artworks


# Create your views here
def index(request):
    return render(request, "artvault/index.html", {"art": artworks})


def blabla(request): ...


def browse_artwork(request):
    return render(request, "artvault/browse_artwork.html", {"art": artworks})

def artwork_details(request, id):
    art = [x for x in artworks if x.id == id][0]
    return render(request, "artvault/artwork_details.html", {
        "art": artworks})