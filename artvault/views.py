from collections import defaultdict
from django.shortcuts import render, get_object_or_404
from django.db.models import Max, Q
from user.models import SellerProfileModel
from artvault.models import Artwork, Bid, Artmovement, ArtmovementArtist
from bids.views import render_artwork_bid, close_auction
from random import shuffle
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from utils.formatting import format_currency


# Create your views here
def index(request):
    all_artworks = Artwork.objects.all()
    for artwork in all_artworks:
        close_auction(artwork)
    artworks = Artwork.objects.filter(sold=False)

    artmovement = defaultdict(list)

    for artwork in artworks:
        artmovement[artwork.art_movement].append(artwork)

    return render(request, "artvault/index.html", {
        "art": Artwork.objects.all(),
        "artmovement": dict(artmovement),
    })


def browse_artwork(request):
    art = Artwork.objects.select_related("seller").prefetch_related("images").annotate(
        highest_bid=Max("bids__amount")
    )

    art_movements = Artwork.objects.values_list("art_movement", flat=True).distinct()

    mediums = Artwork.objects.values_list("medium", flat=True).distinct()

    # search bar
    query = request.GET.get("searchbar")

    if query:
        art = art.filter(
            Q(title__icontains=query)
            | Q(artist_name__icontains=query)
            | Q(medium__icontains=query)
            | Q(art_movement__icontains=query)
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

    # radiobutton sold/on sale
    sale_status = request.GET.get("sale_status")
    now = timezone.now()

    if sale_status == "sold":
        art = art.filter(sold=True)

    elif sale_status == "for_sale":
        art = art.filter(sold=False, auction_end_date__gt=now)

    # current price variable

    for artwork in art:
        starting_price = int(artwork.starting_price)

        if artwork.highest_bid and artwork.highest_bid >= starting_price:
            artwork.current_price = artwork.highest_bid
            artwork.filter_price = artwork.highest_bid
        else:
            artwork.current_price = 0
            artwork.filter_price = starting_price

    # order by price
    if order == "price_low_to_high":
        art = sorted(art, key=lambda artwork: artwork.filter_price)

    elif order == "price_high_to_low":
        art = sorted(art, key=lambda artwork: artwork.filter_price, reverse=True)

    # price range filter
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")

    # price slider filter
    slider_max_price = max(
        [artwork.filter_price for artwork in art],
        default=1000000
    )

    if min_price:
        art = [artwork for artwork in art if artwork.filter_price >= int(min_price)]

    if max_price:
        art = [artwork for artwork in art if artwork.filter_price <= int(max_price)]

    return render(
        request,
        "artvault/browse_artwork.html",
        {
            "art": art,
            "art_movements": art_movements,
            "mediums": mediums,
            "slider_max_price": slider_max_price,
            "selected_min_price": min_price or 0,
            "selected_max_price": max_price or slider_max_price,
        },
    )


def artwork_details(request, id):
    artwork = get_object_or_404(Artwork, pk=id)

    close_auction(artwork)

    user_bid = None

    if request.user.is_authenticated:
        if request.user.profile.role == "buyer":
            user_bid = Bid.objects.filter(
                artwork=artwork,
                buyer=request.user.profile.buyer_profile
            ).first()

    today = timezone.now().date()

    artwork.days_remaining = max((artwork.auction_end_date - today).days, 0)

    auction_over = today >= artwork.auction_end_date

    return render_artwork_bid(request, artwork,auction_over=auction_over, user_bid=user_bid)

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


def public_seller_profile_view(request, id):
    seller = SellerProfileModel.objects.get(pk=id)
    artworks = Artwork.objects.filter(seller=seller)
    print(artworks)
    for artwork in artworks:
        artwork.starting_price = format_currency(int(artwork.starting_price))
    return render(request, "artvault/public_seller_profile.html", {"seller": seller,"artworks":artworks})


def view_sellers(request):
    sellers = SellerProfileModel.objects.all()

    return render(request, "artvault/view_sellers.html", {"sellers": sellers})

def movements(request):
    movements = Artmovement.objects.all()

    for movement in movements:
        artworks = list(movement.artworks.all())
        shuffle(artworks)
        movement.shuffled_artworks = artworks

    return render(request, "artvault/movements.html", {
        "movements": movements,
    })

def movement_artists(request, slug):
    artist = get_object_or_404(ArtmovementArtist,slug=slug)

    return render(request, "artvault/movement_artist.html", {
        "artist": artist,
    })

@login_required
def my_profile_seller(request):
    seller_profile = get_object_or_404(
        SellerProfileModel,
        profile__user=request.user
    )

    seller_artworks = Artwork.objects.filter(
        seller=seller_profile
    ).prefetch_related("images")

    return render(request, "user/my_profile_seller.html", {
        "seller_profile": seller_profile,
        "seller_artworks": seller_artworks,
    })

