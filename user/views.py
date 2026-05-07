from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db import transaction
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from artvault.models import Artwork, Bid
from user.forms.buyerProfileForm import BuyerProfileForm
from user.forms.sellerProfileForm import SellerProfileForm
from user.forms.signupForm import SignupForm
from .models import BuyerProfileModel, Profile, SellerProfileModel

# Create your views here.

# Roles
ALLOWED_ROLE_CHOICES = ["buyer", "individual_seller", "gallery"]


# signup view
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            # Assign role
            role = form.cleaned_data.get("role")
            if role not in ALLOWED_ROLE_CHOICES:
                return HttpResponseForbidden()

            # save after everything has been created
            with transaction.atomic():
                user = form.save()

                group, created = Group.objects.get_or_create(name=role)
                user.groups.add(group)

                Profile.objects.create(user=user, role=role)

            login(request, user)

            if role == "buyer":
                return redirect("buyer_setup")
            else:
                return redirect("seller_setup")

    else:
        form = SignupForm()

    return render(request, template_name="user/signup.html", context={"form": form})


def buyer_setup(request):
    profile = request.user.profile

    buyer_profile_obj, created = BuyerProfileModel.objects.get_or_create(
        profile=profile
    )

    if request.method == "POST":
        form = BuyerProfileForm(request.POST, request.FILES, instance=buyer_profile_obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.profile = profile
            instance.save()

            messages.success(request, "profile_setup_complete")
            return redirect("/")
    else:
        form = BuyerProfileForm(instance=buyer_profile_obj)

    return render(
        request,
        template_name="user/buyer_setup.html",
        context={
            "form": form })


def seller_setup(request):
    profile = request.user.profile
    seller_profile_obj, created = SellerProfileModel.objects.get_or_create(
        profile=profile
    )

    if request.method == "POST":
        form = SellerProfileForm(
            request.POST, request.FILES, instance=seller_profile_obj
        )
        if form.is_valid():
            instance = form.save(commit=False)
            instance.profile = profile
            instance.save()

            messages.success(request, "profile_setup_complete")
            return redirect("/")

    return render(
        request,
        template_name="user/seller_setup.html",
        context={
            "form": SellerProfileForm(instance=seller_profile_obj),
        },
    )


def finalize_bid(request, bid_id):
    print("finalize_bid page")
    print(f"{bid_id}")
    return HttpResponse(content=b"finalize_bid")


# view for viewing your own profile
@login_required
def my_profile_seller(request):
    seller_profile = request.user.profile.seller_profile

    artworks = seller_profile.artworks.all()

    return render(
        request,
        "user/my_profile_seller.html",
        {
            "seller_profile": seller_profile,
            "artworks": artworks,
        },
    )


@login_required
def account_settings(request):
    profile = request.user.profile

    buyer_profile = None
    seller_profile = None

    if profile.role == "buyer":
        buyer_profile = BuyerProfileModel.objects.filter(profile=profile).first()

        if request.method == "POST":
            if "edit-name" in request.POST:
                buyer_profile.full_name = request.POST.get("edit-name")

            if "edit-profile-picture" in request.POST:
                buyer_profile.profile_image = request.POST.get("edit-profile-picture")

            buyer_profile.save()

    else:
        seller_profile = SellerProfileModel.objects.filter(profile=profile).first()

        if request.method == "POST":
            if "edit-name" in request.POST:
                seller_profile.seller_name = request.POST.get("edit-name")

            if "edit-profile-picture" in request.POST:
                seller_profile.logo = request.POST.get("edit-profile-picture")

            if "edit-bio" in request.POST:
                seller_profile.bio = request.POST.get("edit-bio")

            if "edit-street_name" in request.POST:
                seller_profile.street_name = request.POST.get("edit-street_name")
                seller_profile.city = request.POST.get("edit-city")
                seller_profile.zip_code = request.POST.get("edit-zip")

            seller_profile.save()

    return render(
        request,
        "user/account_settings.html",
        {
            "profile": profile,
            "buyer_profile": buyer_profile,
            "seller_profile": seller_profile,
        },
    )
