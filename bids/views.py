from django.contrib.auth.views import login_required
from django.db.models import Max
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from bids.forms.shippingForm import ShippingForm
from bids.forms.bankTransferForm import BankTransferForm
from bids.forms.wireTransferForm import WireTransferForm
from bids.forms.creditCardForm import CreditCardForm
from bids.models import (
    ShippingModel,
    BankTransferModel,
    WireTransferModel,
    CreditCardModel,
)
from artvault.models import Bid, Artwork
from django.contrib import messages
from user.models import BuyerProfileModel
from utils.formatting import format_currency
import math


# Create your views here.


def shipping(request, bid_id):
    bid = get_object_or_404(Bid,pk=bid_id)
    if request.method == "POST":
        form = ShippingForm(request.POST)

        if form.is_valid():
            request.session["shipping_data"] = form.cleaned_data
            return redirect("payment_method", bid_id=bid.pk)

    else:
        form = ShippingForm(initial=request.session.get("shipping_data"))
    return render(request, template_name="bids/shipping.html", context={
        "form": form,
        "bid": bid,
        "artwork": bid.artwork,
        "total_price": format_currency(bid.amount),
    })



def payment_method(request, bid_id):
    bid = get_object_or_404(Bid,pk=bid_id)
    artwork = bid.artwork
    total_price = bid.amount

    if request.method == "POST":
        method = request.POST.get("payment_method")
        request.session["payment_method"] = method

        if method == "card":
            return redirect("credit_card_payment", bid_id=bid.pk)
        elif method == "bank":
            return redirect("bank_transfer_payment", bid_id=bid.pk)
        elif method == "wire":
            return redirect("wire_transfer_payment", bid_id=bid.pk)

    return render(request, "bids/payment_method.html", {
        "bid": bid,
        "artwork": artwork,
        "total_price": format_currency(total_price),
    })


def credit_card_payment(request, shipping_id):
    shipping_obj = get_object_or_404(
        ShippingModel.objects.select_related("bid", "bid__artwork"),
        id=shipping_id
    )

    bid = shipping_obj.bid
    artwork = bid.artwork
    total_price = bid.amount

    payment_obj, created = CreditCardModel.objects.get_or_create(shipping=shipping_obj)

    if request.method == "POST":
        form = CreditCardForm(request.POST, instance=payment_obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.shipping = shipping_obj
            instance.save()
            return redirect("checkout_overview", shipping_id=shipping_obj.id)
    else:
        form = CreditCardForm(instance=payment_obj)

    return render(
        request, "bids/card_payment.html", {
            "form": form,
            "shipping": shipping_obj,
            "bid": bid,
            "artwork": artwork,
            "total_price": format_currency(total_price),
        }
    )


def bank_transfer_payment(request, shipping_id):
    shipping_obj = get_object_or_404(
        ShippingModel.objects.select_related("bid", "bid__artwork"),
        id=shipping_id
    )

    bid = shipping_obj.bid
    artwork = bid.artwork
    total_price = bid.amount

    payment_obj, created = BankTransferModel.objects.get_or_create(
        shipping=shipping_obj
    )

    if request.method == "POST":
        form = BankTransferForm(request.POST, instance=payment_obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.shipping = shipping_obj
            instance.save()
            return redirect("checkout_overview", shipping_id=shipping_obj.id)
    else:
        form = BankTransferForm(instance=payment_obj)

    return render(
        request, "bids/bank_payment.html", {
            "form": form,
            "shipping": shipping_obj,
            "bid": bid,
            "artwork": artwork,
            "total_price": format_currency(total_price),
        }
    )


def wire_transfer_payment(request, shipping_id):
    shipping_obj = get_object_or_404(
        ShippingModel.objects.select_related("bid", "bid__artwork"),
        id=shipping_id
    )

    bid = shipping_obj.bid
    artwork = bid.artwork
    total_price = bid.amount

    payment_obj, created = WireTransferModel.objects.get_or_create(
        shipping=shipping_obj
    )

    if request.method == "POST":
        form = WireTransferForm(request.POST, instance=payment_obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.shipping = shipping_obj
            instance.save()
            return redirect("checkout_overview", shipping_id=shipping_obj.id)
    else:
        form = WireTransferForm(instance=payment_obj)

    return render(
        request, "bids/wire_payment.html", {
            "form": form,
            "shipping": shipping_obj,
            "bid": bid,
            "artwork": artwork,
            "total_price": format_currency(total_price),
        }
    )


def checkout_overview(request, shipping_id):
    shipping_obj = get_object_or_404(
        ShippingModel.objects.select_related("bid", "bid__artwork"),
        id=shipping_id
    )

    bid = shipping_obj.bid
    artwork = bid.artwork
    total_price = bid.amount

    payment = None
    if shipping_obj.payment_method == "card":
        payment = CreditCardModel.objects.get(shipping=shipping_obj)
    elif shipping_obj.payment_method == "bank":
        payment = BankTransferModel.objects.get(shipping=shipping_obj)
    elif shipping_obj.payment_method == "wire":
        payment = WireTransferModel.objects.get(shipping=shipping_obj)

    if request.method == "POST":
        bid = shipping_obj.bid
        artwork = bid.artwork

        artwork.sold = True
        artwork.save()

        bid.status = "completed"
        bid.save()
        messages.success(request, "payment_successful")
        return redirect("/")

    return render(
        request, "bids/overview.html", {
            "shipping": shipping_obj,
            "payment": payment,
            "bid": bid,
            "artwork": artwork,
            "total_price": format_currency(total_price),
        }
    )


@login_required
def my_bids(request):
    profile: BuyerProfileModel = request.user.profile.buyer_profile

    bids = Bid.objects.filter(
        buyer=profile
    ).select_related("artwork").annotate(
        artwork_highest_bid=Max("artwork__bids__amount")
    ).order_by("artwork", "-amount")

    for bid in bids:
        bid.highest_bid = format_currency(bid.artwork_highest_bid)

    return render(
        request,
        "bids/my_bids.html",
        {
            "profile": profile,
            "bids": bids,
        },
    )


def render_artwork_bid(request, artwork, bid_step=None, amount=None, auction_over=False, user_bid=None, minimum_bid=None):
    highest_bid = artwork.bids.order_by("-amount").first()
    current_price = highest_bid.amount if highest_bid else artwork.starting_price
    artwork.days_remaining = (artwork.auction_end_date - timezone.now().date()).days

    return render(
        request,
        "artvault/artwork_details.html",
        {
            "artwork": artwork,
            "highest_bid": highest_bid,
            "current_price": format_currency(current_price),
            "bid_step": bid_step,
            "amount": amount,
            "auction_over": auction_over,
            "user_bid": user_bid,
            "minimum_bid": minimum_bid,
        },
    )


@login_required
def make_bid(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)

    buyer_profile = request.user.profile.buyer_profile

    user_bid = Bid.objects.filter(
        artwork=artwork,
        buyer=buyer_profile
    ).order_by("-timestamp").first()

    highest_bid = Bid.objects.filter(artwork=artwork).order_by("-amount").first()
    current_price = highest_bid.amount if highest_bid else artwork.starting_price

    has_bid = artwork.bids.exists()
    max_bid = 2147483647

    if has_bid:
        minimum_bid = math.ceil(current_price * 1.10 / 1000) * 1000
    else:
        minimum_bid = int(artwork.starting_price)

    if request.method == "POST":

        amount = request.POST.get("amount")

        if not amount:
            messages.error(request, "Please enter a bid amount")
            return redirect("make_bid", artwork_id)

        if "." in amount:
            messages.error(request, "Bid amount must be a whole number.")
            return redirect("make_bid", artwork_id)

        try:
            amount = int(amount)
        except ValueError:
            messages.error(request, "Please enter a valid number.")
            return redirect("make_bid", artwork_id)
        if amount < minimum_bid:
            messages.error(
                request, f"Your bid must be at least {minimum_bid} Kr."
            )
            return redirect("make_bid", artwork_id)
        if amount > max_bid:
            messages.error(request,"Bid is too large")
            return redirect("make_bid",artwork_id)

        request.session["pending_bid_amount"] = amount
        return render_artwork_bid(request, artwork, "confirm", amount, user_bid=user_bid, minimum_bid=minimum_bid)

    return render_artwork_bid(request, artwork, "make", user_bid=user_bid, minimum_bid=minimum_bid)


@login_required
def submit_bid(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)

    if request.method != "POST":
        return redirect("artwork-details", artwork_id)

    amount = request.session.get("pending_bid_amount")

    if not amount:
        messages.error(request, "No bid amount found")
        return redirect("artwork-details", artwork_id)

    Bid.objects.create(
        artwork=artwork,
        amount=amount,
        buyer=request.user.profile.buyer_profile,
        status="pending",
    )

    request.session.pop("pending_bid_amount", None)

    return render_artwork_bid(request, artwork, "success", amount)


@login_required
def accept_bid(request, bid_id):
    bid = get_object_or_404(Bid, id=bid_id)

    artwork = bid.artwork

    if artwork.is_closed:
        return redirect("artwork-details", artwork.id)

    artwork.bids.exclude(id=bid.id).update(status="rejected")

    bid.status = "accepted"
    bid.save()

    artwork.is_closed = True
    artwork.save()

    return redirect(request.META.get("HTTP_REFERER"))


def close_auction(artwork):
    today = timezone.now().date()

    if today >= artwork.auction_end_date and not artwork.is_closed:
        highest_bid = artwork.bids.order_by("-amount").first()

        if highest_bid:
            artwork.bids.exclude(id=highest_bid.id).update(status="rejected")
            highest_bid.status = "accepted"
            highest_bid.save()

        artwork.is_closed = True
        artwork.save()
