from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from django.contrib import messages
from artvault.models import Artwork, ArtworkImage
from listings.forms.listing_form import ArtworkListingForm

# Create your views here.


def add_listing_view(request):
    profile = request.user.profile

    if profile.role == "buyer":
        return HttpResponseForbidden("Only sellers can add listings.")

    seller_profile = profile.seller_profile

    if request.method == "POST":
        form = ArtworkListingForm(request.POST, request.FILES)

        if form.is_valid():
            print("form is valid")
            artwork = form.save(commit=False)
            artwork.seller = seller_profile
            artwork.sold = False
            artwork.save()

            images = request.FILES.getlist("images")
            messages.success(request, "listing_created")

            for image in images:
                ArtworkImage.objects.create(artwork=artwork, image=image)

            return redirect("my_profile_seller")
        else:
            print(form.errors)

    else:
        print("form is not valid")
        form = ArtworkListingForm()

    return render(request, "listings/add_listing.html", {"form": form})


def my_listing_view(request, id):
    artwork = Artwork.objects.get(pk=id)
    bids = artwork.bids.all().order_by("-amount")
    auction_over = False
    if timezone.now().date() > artwork.auction_end_date:
        auction_over = True
    return render(
        request,
        "listings/my_listing.html",
        {
            "artwork": artwork,
            "bids": bids,
            "auction_over": auction_over,
        },
    )

def delete_listing_view(request, id):
    artwork = get_object_or_404(Artwork, pk=id)
    artwork.delete()
    return redirect("my_profile_seller")
