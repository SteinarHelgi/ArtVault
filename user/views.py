from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
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

            request.session["signup_data"] = {
                "username": form.cleaned_data["username"],
                "password": form.cleaned_data["password1"],
                "role": role,
            }

            if role == "buyer":
                return redirect("buyer-setup")
            else:
                return redirect("seller-setup")

    else:
        form = SignupForm()

    return render(request, template_name="user/signup.html", context={"form": form})


def buyer_setup(request):
    signup_data = request.session.get("signup_data")

    if not signup_data:
        return redirect("signup")


    if request.method == "POST":
        form = BuyerProfileForm(request.POST, request.FILES)

        if form.is_valid():
            with transaction.atomic():
                user = User.objects.create_user(
                    username=signup_data["username"],
                    password=signup_data["password"],
                )

                role = signup_data["role"]

                group, created = Group.objects.get_or_create(name=role)
                user.groups.add(group)

                profile = Profile.objects.create(user=user, role=role)

                buyer_profile = form.save(commit=False)
                buyer_profile.profile = profile
                buyer_profile.save()

            login(request, user)

            request.session.pop("signup_data", None)

            messages.success(request, "profile_setup_complete")
            return redirect("/")
    else:
        form = BuyerProfileForm()

    return render(request, "user/buyer_setup.html", {"form": form})

def seller_setup(request):
    signup_data = request.session.get("signup_data")

    if not signup_data:
        return redirect("signup")

    if request.method == "POST":
        form = SellerProfileForm(request.POST, request.FILES)

        if form.is_valid():
            with transaction.atomic():
                user = User.objects.create_user(
                    username=signup_data["username"],
                    password=signup_data["password"],
                )

                role = signup_data["role"]

                group, created = Group.objects.get_or_create(name=role)
                user.groups.add(group)

                profile = Profile.objects.create(
                    user=user,
                    role=role
                )

                seller_profile = form.save(commit=False)
                seller_profile.profile = profile
                seller_profile.save()

            login(request, user)

            request.session.pop("signup_data", None)

            messages.success(request, "profile_setup_complete")
            return redirect("/")
    else:
        form = SellerProfileForm()

    return render(request, "user/seller_setup.html", {
        "form": form,
    })



# view for viewing your own profile
@login_required
def my_profile_seller(request):
    seller_profile = request.user.profile.seller_profile

    artworks = seller_profile.artworks.prefetch_related("images").annotate(
        highest_bid=Max("bids__amount")
    )
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
