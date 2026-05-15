from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from django.contrib import messages
from artvault.models import Artwork, ArtworkImage
from listings.forms.listing_form import ArtworkListingForm


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
            images = request.FILES.getlist("images")

            if not images:
                form.add_error(None, "Please upload at least one artwork image.")
                return render(request, "listings/add_listing.html", {
                    "form": form
                })

            if len(images) > 3:
                form.add_error(None, "You can upload a maximum of 3 images.")
                return render(request, "listings/add_listing.html", {
                    "form": form
                })

            artwork = form.save(commit=False)
            artwork.seller = seller_profile
            artwork.sold = False
            artwork.save()

            messages.success(request, "listing_created")

            for image in images:
                ArtworkImage.objects.create(artwork=artwork, image=image)

            return redirect("my-profile-seller")

    else:
        form = ArtworkListingForm()

    return render(request, "listings/add_listing.html", {"form": form})


@login_required
def my_listing_view(request, id):
    artwork = get_object_or_404(
        Artwork.objects.select_related("seller").prefetch_related("images"),
        pk=id
    )

    bids = list(
        artwork.bids.select_related("buyer").order_by("-amount")
    )

    highest_bid = bids[0] if bids else None

    today = timezone.now().date()

    artwork.days_remaining = max((artwork.auction_end_date - today).days, 0)

    auction_over = today >= artwork.auction_end_date

    return render(
        request,
        "listings/my_listing.html",
        {
            "artwork": artwork,
            "bids": bids,
            "auction_over": auction_over,
            "highest_bid": highest_bid,
        },
    )


@login_required
def delete_listing_view(request, id):
    artwork = get_object_or_404(
        Artwork,
        pk=id,
        seller=request.user.profile.seller_profile
    )

    artwork.delete()
    return redirect("my-profile-seller")


@login_required
def update_listing_view(request, id):
    artwork = get_object_or_404(
        Artwork.objects.select_related("seller").prefetch_related("images"),
        pk=id
    )

    if artwork.seller != request.user.profile.seller_profile:
        return HttpResponseForbidden("You can only update your own listings.")

    if request.method == "POST":
        form = ArtworkListingForm(request.POST, request.FILES, instance=artwork)

        if form.is_valid():
            images = request.FILES.getlist("images")

            if len(images) > 3:
                form.add_error(None, "You can upload a maximum of 3 images.")
                return render(request, "listings/update_listing.html", {
                    'id': id,
                    'form': form,
                    'artwork': artwork,
                })

            artwork = form.save()

            if images:
                artwork.images.all().delete()

                for image in images:
                    ArtworkImage.objects.create(
                        artwork=artwork,
                        image=image
                    )

            return redirect("my-listing", id=id)

    else:
        form = ArtworkListingForm(instance=artwork)

    return render(request, "listings/update_listing.html", {
        'id': id,
        'form': form,
        'artwork': artwork,
    })
