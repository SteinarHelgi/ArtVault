from collections import defaultdict
from django.shortcuts import render
from django.db.models import Max
from artvault.models import Artwork, Bid


# Create your views here
def index(request):
    return render(request, "artvault/index.html", {"art": Artwork.objects.all()})


def blabla(request): ...


def browse_artwork(request):
    art = Artwork.objects.prefetch_related("images", "bid_set")

    for artwork in art:
        highest_bid = artwork.bid_set.aggregate(Max("amount"))["amount__max"]

        if highest_bid and highest_bid >= int(artwork.starting_price):
            artwork.current_price = highest_bid
        else:
            artwork.current_price = 0

    return render(
        request,
        "artvault/browse_artwork.html",
        {"art": art},
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

















