from collections import defaultdict
from django.shortcuts import render
from django.db.models import Max, Q
from artvault.models import Artwork


# Create your views here
def index(request):
    return render(request, "artvault/index.html", {"art": Artwork.objects.all()})


def blabla(request): ...


def browse_artwork(request):
    art = Artwork.objects.prefetch_related("images", "bid_set")

    art_movements = Artwork.objects.values_list(
        "art_movement",
        flat=True
    ).distinct()

    mediums = Artwork.objects.values_list(
        "medium",
        flat=True
    ).distinct()

    # search bar
    query = request.GET.get("searchbar")

    if query:
        art = art.filter(
            Q(title__icontains=query) |
            Q(artist_name__icontains=query) |
            Q(medium__icontains=query) |
            Q(art_movement__icontains=query)
        )

    # art movement filter
    movement = request.GET.get("movement")

    if movement:
        art = art.filter(art_movement__iexact=movement.strip())

    # medium filter
    medium = request.GET.get("medium")

    if medium:
        art = art.filter(medium__iexact=medium.strip())

    # order by filter
    order = request.GET.get("order")

    if order == "title":
        art = art.order_by("title")

    elif order == "artist":
        art = art.order_by("artist_name")

    # current price variable
    for artwork in art:
        highest_bid = artwork.bid_set.aggregate(Max("amount"))["amount__max"]

        if highest_bid and highest_bid >= int(artwork.starting_price):
            artwork.current_price = highest_bid
        else:
            artwork.current_price = 0

    return render(
        request,
        "artvault/browse_artwork.html",
        {
            "art": art,
            "art_movements": art_movements,
            "mediums": mediums,
        },
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

















