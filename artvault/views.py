from collections import defaultdict
from django.shortcuts import render

from artvault.models import Artwork



# Create your views here
def index(request):
    return render(request, "artvault/index.html", {"art": Artwork.objects.all()})


def blabla(request): ...


def browse_artwork(request):
    return render(
        request, "artvault/browse_artwork.html", {"art": Artwork.objects.all()}
    )


def artwork_details(request, id):
    return render(
        request,
        "artvault/artwork_details.html",
        {"art": Artwork.objects.all(), "id": id},
    )

def browse_artists(request):
    artworks = Artwork.objects.prefetch_related("images").all()

    artists = defaultdict(list)


    for artwork in artworks:
        artists[artwork.artist_name].append(artwork)

    for artist in artists:
        print(artist)

    return render(
        request,
        "artvault/browse_artists.html",
        {
            "artists": dict(artists),
        },
    )

















