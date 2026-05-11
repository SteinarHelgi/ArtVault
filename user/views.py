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
from user.forms.accountSettingsForm import BuyerAccountSettingsForm, IndividualSellerAccountSettingsForm, GalleryAccountSettingsForm
from .models import BuyerProfileModel, Profile, SellerProfileModel
from django.contrib.auth import get_user_model

from django.db.models import Max
# Create your views here.

# Roles
ALLOWED_ROLE_CHOICES = ["buyer", "individual_seller", "gallery"]

User = get_user_model()

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

            request.session["pending_user_id"] = user.id
            request.session["pending_role"] = role

            if role == "buyer":
                return redirect("buyer_setup")
            else:
                return redirect("seller_setup")

    else:
        form = SignupForm()

    return render(request, template_name="user/signup.html", context={"form": form})


def buyer_setup(request):
    pending_user_id = request.session["pending_user_id"]

    if not pending_user_id:
        return redirect("signup")

    user = User.objects.get(id=pending_user_id)
    profile = user.profile

    buyer_profile_obj, created = BuyerProfileModel.objects.get_or_create(
        profile=profile
    )

    if request.method == "POST":
        form = BuyerProfileForm(request.POST, request.FILES, instance=buyer_profile_obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.profile = profile
            instance.save()

            login(request, user)

            request.session.pop("pending_user_id", None)
            request.session.pop("pending_role", None)

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
    pending_user_id = request.session["pending_user_id"]

    if not pending_user_id:
        return redirect("signup")

    user = User.objects.get(id=pending_user_id)
    profile = user.profile

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

            login(request, user)

            request.session.pop("pending_user_id", None)
            request.session.pop("pending_role", None)

            messages.success(request, "profile_setup_complete")
            return redirect("/")
    else:
        form = SellerProfileForm(instance=seller_profile_obj)

    return render(
        request,
        template_name="user/seller_setup.html",
        context={
            "form": form,
        })

# view for viewing your own profile
@login_required
def my_profile_seller(request):
    seller_profile = request.user.profile.seller_profile

    artworks = seller_profile.artworks.annotate(
        highest_bid=Max("bids__amount")
    )
    messages.success(request, "listing_created")
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

    if profile.role == "buyer":
        account_profile = profile.buyer_profile
        form_class = BuyerAccountSettingsForm

    elif profile.role == "gallery":
        account_profile = profile.seller_profile
        form_class = GalleryAccountSettingsForm

    else:
        account_profile = profile.seller_profile
        form_class = IndividualSellerAccountSettingsForm

    if request.method == "POST":
        form = form_class(request.POST, request.FILES, instance=account_profile)

        if form.is_valid():
            form.save()

            new_password = form.cleaned_data.get("new_password")

            if new_password:
                request.user.set_password(new_password)
                request.user.save()
                login(request, request.user)

            messages.success(request, "account-settings-updated")
            return redirect("account-settings")
        else:
            messages.error(request, "account-settings-update-failed")
    else:
        form = form_class(instance=account_profile)

    return render(request, "user/account_settings.html", {
        "form": form,
        "profile": profile,
    })
