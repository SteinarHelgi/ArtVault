from collections import defaultdict
from django.shortcuts import render, get_object_or_404
from django.db.models import Max, Q
from user.models import SellerProfileModel
from artvault.models import Artwork, Bid, Artmovement, ArtmovementArtist
from bids.views import render_artwork_bid, close_auction
from random import shuffle
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from utils.formatting import format_currency
from django.contrib import messages


# Create your views here
def index(request):
    today = timezone.now().date()

    expired_artworks = Artwork.objects.filter(
        auction_end_date__lte=today,
        is_closed=False,
    )

    for artwork in expired_artworks:
        close_auction(artwork)

    artworks = Artwork.objects.filter(is_closed=False).prefetch_related("images")

    artmovement = defaultdict(list)

    for artwork in artworks:
        artmovement[artwork.art_movement].append(artwork)

    return render(request, "artvault/index.html", {
        "art": artworks,
        "artmovement": dict(artmovement),
    })


def browse_artwork(request):
    today = timezone.now().date()

    expired_artworks = Artwork.objects.filter(
        auction_end_date__lte=today,
        is_closed=False,
    )

    for artwork in expired_artworks:
        close_auction(artwork)

    art = Artwork.objects.only(
        "id",
        "title",
        "artist_name",
        "starting_price",
        "medium",
        "art_movement",
        "dimensions",
        "auction_end_date",
        "is_closed",
    ).prefetch_related("images").annotate(
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

    # radiobutton auction status
    sale_status = request.GET.get("sale_status")

    if sale_status == "closed":
        art = art.filter(is_closed=True)

    elif sale_status == "open":
        art = art.filter(is_closed=False, auction_end_date__gt=today)

    # order by filter
    order = request.GET.get("order")

    if order == "title":
        art = art.order_by("title")

    elif order == "artist":
        art = art.order_by("artist_name")

    # current price variable
    for artwork in art:
        starting_price = int(artwork.starting_price)

        artwork.formatted_starting_price = format_currency(starting_price)
        artwork.filter_price = starting_price

        if artwork.highest_bid and artwork.highest_bid >= starting_price:
            artwork.current_price = format_currency(artwork.highest_bid)
            artwork.filter_price = artwork.highest_bid
        else:
            artwork.current_price = 0
        

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

    if not order:
        art = sorted(art, key=lambda artwork: artwork.id, reverse=True)

    paginator = Paginator(art, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()

    if "page" in query_params:
        query_params.pop("page")

    query_string = query_params.urlencode()

    return render(
        request,
        "artvault/browse_artwork.html",
        {
            "art": page_obj,
            "page_obj": page_obj,
            "query_string": query_string,
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
            ).order_by("-id").first()

    today = timezone.now().date()

    artwork.days_remaining = max((artwork.auction_end_date - today).days, 0)

    auction_over = today >= artwork.auction_end_date

    return render_artwork_bid(request, artwork,auction_over=auction_over, user_bid=user_bid)

def browse_artists(request):
    artworks = Artwork.objects.prefetch_related("images").all()

    artists = defaultdict(list)

    for artwork in artworks:
        artists[artwork.artist_name].append(artwork)

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


#Footer links
def contact_us(request):
    if request.method == "POST":
        messages.success(request, "message_sent")
    return render(request, "artvault/contact_us.html")

def common_questions(request):
    return render(request, "artvault/common_questions.html")

def about_us(request):
    return render(request, "artvault/about_us.html")

def terms_and_conditions(request):
    return render(request, "artvault/terms_and_conditions.html")
