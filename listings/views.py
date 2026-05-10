from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

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
            artwork = form.save(commit=False)
            artwork.seller = seller_profile
            artwork.save()

            ArtworkImage.objects.create(
                artwork=artwork,
                image=form.cleaned_data["image"],
            )

            return redirect("my_profile_seller")
    else:
        form = ArtworkListingForm()

    return render(request, "listings/add_listing.html", {"form": form})


def my_listing_view(request, id):
    artwork = Artwork.objects.get(pk=id)
    bids = artwork.bids.all().order_by('-amount')
    return render(request, "listings/my_listing.html", {"artwork": artwork,"bids": bids})
