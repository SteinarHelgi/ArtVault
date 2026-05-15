from django.contrib.auth.views import login_required
from django.db.models import Max
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from bids.forms.shippingForm import ShippingForm
from bids.forms.bankTransferForm import BankTransferForm
from bids.forms.wireTransferForm import WireTransferForm
from bids.forms.creditCardForm import CreditCardForm
from artvault.models import Bid, Artwork
from django.contrib import messages
from bids.models import Order
from user.models import BuyerProfileModel
from utils.formatting import format_currency
import math


# Create your views here.


def shipping(request, bid_id):
    bid = get_object_or_404(Bid, pk=bid_id)
    if request.method == "POST":
        form = ShippingForm(request.POST)

        if form.is_valid():
            request.session["shipping_data"] = form.cleaned_data
            return redirect("payment-method", bid_id=bid.pk)

    else:
        form = ShippingForm(initial=request.session.get("shipping_data"))
    return render(
        request,
        template_name="bids/shipping.html",
        context={
            "form": form,
            "bid": bid,
            "artwork": bid.artwork,
            "total_price": format_currency(bid.amount),
        },
    )


def payment_method(request, bid_id):
    bid = get_object_or_404(Bid, pk=bid_id)
    artwork = bid.artwork
    total_price = bid.amount

    if "shipping_data" not in request.session:
        return redirect("shipping", bid_id=bid.pk)

    if request.method == "POST":
        method = request.POST.get("payment_method")
        request.session["payment_method"] = method

        if method == "card":
            return redirect("credit-card-payment", bid_id=bid.pk)
        elif method == "bank":
            return redirect("bank-transfer-payment", bid_id=bid.pk)
        elif method == "wire":
            return redirect("wire-transfer-payment", bid_id=bid.pk)

    return render(
        request,
        "bids/payment_method.html",
        {
            "bid": bid,
            "artwork": artwork,
            "total_price": format_currency(total_price),
        },
    )


def credit_card_payment(request, bid_id):
    bid = get_object_or_404(Bid, pk=bid_id)

    if "shipping_data" not in request.session:
        return redirect("shipping", bid_id=bid.pk)

    if request.method == "POST":
        form = CreditCardForm(request.POST)

        if form.is_valid():
            request.session["card_data"] = {
                "cardholder_name": form.cleaned_data["cardholder_name"],
                "card_number": form.cleaned_data["card_number"],
                "card_expiration": form.cleaned_data["card_expiration"],
                "card_cvv": form.cleaned_data["card_cvv"],
                "card_last4": form.cleaned_data["card_number"][-4:],
            }
            return redirect("checkout-overview", bid_id=bid.pk)
    else:
        form = CreditCardForm(initial=request.session.get("card_data"))

    return render(
        request,
        "bids/card_payment.html",
        {
            "form": form,
            "bid": bid,
            "artwork": bid.artwork,
            "total_price": format_currency(bid.amount),
        },
    )


def bank_transfer_payment(request, bid_id):
    bid = get_object_or_404(Bid, pk=bid_id)

    if "shipping_data" not in request.session:
        return redirect("shipping", bid_id=bid.pk)

    if request.method == "POST":
        form = BankTransferForm(request.POST)

        if form.is_valid():
            request.session["bank_data"] = form.cleaned_data
            return redirect("checkout-overview", bid_id=bid.pk)
    else:
        form = BankTransferForm(initial=request.session.get("bank_data"))

    return render(
        request,
        "bids/bank_payment.html",
        {
            "form": form,
            "bid": bid,
            "artwork": bid.artwork,
            "total_price": format_currency(bid.amount),
        },
    )


def wire_transfer_payment(request, bid_id):
    bid = get_object_or_404(Bid, pk=bid_id)

    if "shipping_data" not in request.session:
        return redirect("shipping", bid_id=bid.pk)

    if request.method == "POST":
        form = WireTransferForm(request.POST)

        if form.is_valid():
            request.session["wire_data"] = form.cleaned_data
            return redirect("checkout-overview", bid_id=bid.pk)
    else:
        form = WireTransferForm(initial=request.session.get("wire_data"))

    return render(
        request,
        "bids/wire_payment.html",
        {
            "form": form,
            "bid": bid,
            "artwork": bid.artwork,
            "total_price": format_currency(bid.amount),
        },
    )


def checkout_overview(request, bid_id):
    bid = get_object_or_404(
        Bid.objects.select_related("artwork"),
        pk=bid_id,
    )

    artwork = bid.artwork
    total_price = bid.amount

    shipping = request.session.get("shipping_data")
    payment_method = request.session.get("payment_method")

    if not shipping:
        return redirect("shipping", bid_id=bid.pk)

    if not payment_method:
        return redirect("payment-method", bid_id=bid.pk)

    payment = None

    if payment_method == "card":
        payment = request.session.get("card_data")
    elif payment_method == "bank":
        payment = request.session.get("bank_data")
    elif payment_method == "wire":
        payment = request.session.get("wire_data")

    if not payment:
        return redirect("payment-method", bid_id=bid.pk)

    if request.method == "POST":
        artwork.sold = True
        artwork.save()

        bid.status = "completed"
        bid.save()

        Order.objects.create(
            artwork=artwork,
            buyer=bid.buyer,
            seller=artwork.seller,
            bid=bid,
        )

        request.session.pop("shipping_data", None)
        request.session.pop("payment_method", None)
        request.session.pop("card_data", None)
        request.session.pop("bank_data", None)
        request.session.pop("wire_data", None)

        messages.success(request, "payment_successful")
        return redirect("/")

    return render(
        request,
        "bids/overview.html",
        {
            "shipping": shipping,
            "payment_method": payment_method,
            "payment": payment,
            "bid": bid,
            "artwork": artwork,
            "total_price": format_currency(total_price),
        },
    )


@login_required
def my_bids(request):
    profile: BuyerProfileModel = request.user.profile.buyer_profile

    bids = (
        Bid.objects.filter(buyer=profile)
        .select_related("artwork")
        .annotate(artwork_highest_bid=Max("artwork__bids__amount"))
        .order_by("artwork", "-amount")
    )

    for bid in bids:
        close_auction(bid.artwork)
        bid.refresh_from_db()
        bid.artwork.refresh_from_db()
        highest_bid = bid.artwork.bids.order_by("-amount").first()
        bid.highest_bid = format_currency(highest_bid.amount)

    return render(
        request,
        "bids/my_bids.html",
        {
            "profile": profile,
            "bids": bids,
        },
    )

def render_artwork_bid(
    request,
    artwork,
    bid_step=None,
    amount=None,
    auction_over=False,
    user_bid=None,
    minimum_bid=None,
):
    close_auction(artwork)

    highest_bid = artwork.bids.order_by("-amount").first()
    current_price = highest_bid.amount if highest_bid else artwork.starting_price
    artwork.days_remaining = (artwork.auction_end_date - timezone.now().date()).days
    auction_over = auction_over or artwork.is_closed or timezone.now().date() >= artwork.auction_end_date

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
    close_auction(artwork)

    if artwork.is_closed:
        messages.error(request, "This auction has ended. You can no longer place a bid.")
        return redirect("artwork-details", artwork_id)

    buyer_profile = request.user.profile.buyer_profile

    user_bid = Bid.objects.filter(
        artwork=artwork,
        buyer=buyer_profile
    ).order_by("-id").first()

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
            return redirect("make-bid", artwork_id)

        if "." in amount:
            messages.error(request, "Bid amount must be a whole number.")
            return redirect("make-bid", artwork_id)

        try:
            amount = int(amount)
        except ValueError:
            messages.error(request, "Please enter a valid number.")
            return redirect("make-bid", artwork_id)
        if amount < minimum_bid:
            messages.error(
                request, f"Your bid must be at least {minimum_bid} kr."
            )
            return redirect("make-bid", artwork_id)
        if amount > max_bid:
            messages.error(request, "Bid is too large")
            return redirect("make-bid", artwork_id)

        request.session["pending_bid_amount"] = amount
        return render_artwork_bid(
            request,
            artwork,
            "confirm",
            amount,
            user_bid=user_bid,
            minimum_bid=minimum_bid,
        )

    return render_artwork_bid(
        request, artwork, "make", user_bid=user_bid, minimum_bid=minimum_bid
    )


@login_required
def submit_bid(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    close_auction(artwork)

    if artwork.is_closed:
        request.session.pop("pending_bid_amount", None)
        messages.error(request, "This auction has ended. Your bid was not submitted.")
        return redirect("artwork-details", artwork_id)

    if request.method != "POST":
        return redirect("artwork-details", artwork_id)

    amount = request.session.get("pending_bid_amount")

    if not amount:
        messages.error(request, "No bid amount found")
        return redirect("artwork-details", artwork_id)

    new_bid = Bid.objects.create(
        artwork=artwork,
        amount=amount,
        buyer=request.user.profile.buyer_profile,
        status="pending",
    )

    request.session.pop("pending_bid_amount", None)

    return render_artwork_bid(request, artwork, "success", amount, user_bid=new_bid)


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
