from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from artvault.models import ArtworkImage
from listings.forms.listing_form import ArtworkListingForm

# Create your views here.


def add_listing_view(request):
    profile = request.user.profile

    if profile.role == "buyer":
        return HttpResponseForbidden("Only sellers can add listings.")

    seller_profile = profile.seller_profile

    if request.method == "POST":
        form = ArtworkListingForm(request.POST)

        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.seller = seller_profile
            artwork.save()

            ArtworkImage.objects.create(
                artwork=artwork,
                image_path=form.cleaned_data["image_path"],
            )

            return redirect("my_profile_seller")
    else:
        form = ArtworkListingForm()

    return render(request, "listings/add_listing.html", {"form": form})


# def my_listings_view(request):
#     profile = user.profile.sellerprofilemodel
