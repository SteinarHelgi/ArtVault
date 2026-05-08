from django.contrib.auth.views import login_required
from django.shortcuts import render, redirect,get_object_or_404
from bids.forms.shippingForm import ShippingForm
from bids.forms.bankTransferForm import BankTransferForm
from bids.forms.wireTransferForm import WireTransferForm
from bids.forms.creditCardForm import CreditCardForm
from bids.models import ShippingModel, BankTransferModel, WireTransferModel, CreditCardModel
from artvault.models import Bid, Artwork
from django.contrib import messages

from user.models import BuyerProfileModel, Profile, SellerProfileModel
# Create your views here.

def shipping(request,bid_id):
    bid = Bid.objects.get(id=bid_id)
    if request.method == 'POST':
        form = ShippingForm(request.POST)

        if form.is_valid():
            shipping_obj = form.save()
            shipping_obj.bid = bid
            shipping_obj.save()
            return redirect("payment_method", shipping_id=shipping_obj.id)

    else:
        form = ShippingForm()
    return render(request, template_name='bids/shipping.html', context={'form': form})

def shipping_edit(request, shipping_id):
    shipping_obj = ShippingModel.objects.get(id=shipping_id)

    if request.method == "POST":
        form = ShippingForm(request.POST, instance=shipping_obj)
        if form.is_valid():
            form.save()
            return redirect("payment_method", shipping_id=shipping_obj.id)
    else:
        form = ShippingForm(instance=shipping_obj)

    return render(request, "bids/shipping.html", {
        "form": form,
        "shipping": shipping_obj
    })

def payment_method(request, shipping_id):
    shipping_obj = ShippingModel.objects.get(id=shipping_id)

    if request.method == "POST":
        method = request.POST.get("payment_method")
        shipping_obj.payment_method = method
        shipping_obj.save()

        if method == "card":
            return redirect("credit_card_payment", shipping_id=shipping_obj.id)
        elif method == "bank":
            return redirect("bank_transfer_payment", shipping_id=shipping_obj.id)
        elif method == "wire":
            return redirect("wire_transfer_payment", shipping_id=shipping_obj.id)

    return render(request, "bids/payment_method.html", {"shipping": shipping_obj})

def credit_card_payment(request, shipping_id):
    shipping_obj = ShippingModel.objects.get(id=shipping_id)

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

    return render(request, "bids/card_payment.html", {
        "form": form,
        "shipping": shipping_obj
        })

def bank_transfer_payment(request, shipping_id):
    shipping_obj = ShippingModel.objects.get(id=shipping_id)

    payment_obj, created = BankTransferModel.objects.get_or_create(shipping=shipping_obj)

    if request.method == "POST":
        form = BankTransferForm(request.POST, instance=payment_obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.shipping = shipping_obj
            instance.save()
            return redirect("checkout_overview", shipping_id=shipping_obj.id)
    else:
        form = BankTransferForm(instance=payment_obj)

    return render(request, "bids/bank_payment.html", {
        "form": form,
        "shipping": shipping_obj
        })

def wire_transfer_payment(request, shipping_id):
    shipping_obj = ShippingModel.objects.get(id=shipping_id)

    payment_obj, created = WireTransferModel.objects.get_or_create(shipping=shipping_obj)

    if request.method == "POST":
        form = WireTransferForm(request.POST, instance=payment_obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.shipping = shipping_obj
            instance.save()
            return redirect("checkout_overview", shipping_id=shipping_obj.id)
    else:
        form = WireTransferForm(instance=payment_obj)

    return render(request, "bids/wire_payment.html", {
        "form": form,
        "shipping": shipping_obj
        })

def checkout_overview(request, shipping_id):
    shipping_obj = ShippingModel.objects.get(id=shipping_id)

    payment = None
    if shipping_obj.payment_method == "card":
        payment = CreditCardModel.objects.get(shipping=shipping_obj)
    elif shipping_obj.payment_method == "bank":
        payment = BankTransferModel.objects.get(shipping=shipping_obj)
    elif shipping_obj.payment_method == "wire":
        payment = WireTransferModel.objects.get(shipping=shipping_obj)

    if request.method == "POST":
        messages.success(request, "payment_successful")
        return redirect("/")

    return render(request, "bids/overview.html", {
        "shipping": shipping_obj,
        "payment": payment
    })

@login_required
def my_bids(request):
    profile: BuyerProfileModel = request.user.profile.buyer_profile
    bids = Bid.objects.filter(buyer=profile)

    return render(
        request,
        "bids/my_bids.html",
        {
            "profile": profile,
            "bids": bids,
        },
    )

def render_artwork_bid(request, artwork, bid_step=None, amount=None):
    highest_bid = artwork.bids.order_by("-amount").first()
    current_price = highest_bid.amount if highest_bid else artwork.starting_price

    return render(request, "artvault/artwork_details.html", {
        "artwork": artwork,
        "highest_bid": highest_bid,
        "current_price": current_price,
        "bid_step": bid_step,
        "amount": amount
    })

@login_required
def make_bid(request, artwork_id):
    artwork = get_object_or_404(Artwork,id=artwork_id)

    highest_bid = Bid.objects.filter(artwork=artwork).order_by("-amount").first()
    current_price = highest_bid.amount if highest_bid else artwork.starting_price

    if request.method == "POST":
        amount = request.POST.get("amount")

        if not amount:
            messages.error(request, "Please enter a bid amount")
            return redirect("make_bid", artwork_id)

        amount = int(amount)
        minimum_bid = current_price + 5000

        if amount <  minimum_bid:
            messages.error(request, f"Your bid must be at least {minimum_bid + 5000} Kr.")
            return redirect("make_bid", artwork_id)

        request.session["pending_bid_amount"] = amount
        return render_artwork_bid(request, artwork, "confirm", amount)

    return render_artwork_bid(request, artwork, "make")

@login_required
def submit_bid(request, artwork_id):
    artwork = get_object_or_404(Artwork,id=artwork_id)

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
    )

    request.session.pop("pending_bid_amount", None)

    return render_artwork_bid(request, artwork, "success", amount)






