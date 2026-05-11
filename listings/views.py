from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from django.contrib import messages
from artvault.models import Artwork, ArtworkImage
from listings.forms.listing_form import ArtworkListingForm
from listings.forms.update_listing_form import UpdateArtworkListingForm


# Create your views here.


@login_required
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

@login_required
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
@login_required
def delete_listing_view(request, id):
    artwork = get_object_or_404(Artwork, pk=id)
    artwork.delete()
    return redirect("my_profile_seller")


@login_required
def update_listing_view(request, id):
    artwork = get_object_or_404(Artwork, pk=id)

    if artwork.seller != request.user.profile.seller_profile:
        return HttpResponseForbidden("You can only update your own listings.")

    if request.method == "POST":
        form = UpdateArtworkListingForm(request.POST, request.FILES, instance=artwork)

        if form.is_valid():
            artwork = form.save()

            new_image = form.cleaned_data.get("image")

            if new_image:
                artwork_image = artwork.images.first()

                if artwork_image:
                    artwork_image.image = new_image
                    artwork_image.save()
                else:
                    ArtworkImage.objects.create(
                        artwork=artwork,
                        image=new_image
                    )
            return redirect("my-listing", id=id)

    else:
        form = UpdateArtworkListingForm(instance=artwork)

    return render(request, "listings/update_listing.html", {
        'id': id,
        'form': form,
        'artwork': artwork,
    })