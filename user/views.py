from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import Group
from user.forms.signupForm import SignupForm
from user.forms.buyerProfileForm import BuyerProfileForm
from user.forms.sellerProfileForm import SellerProfileForm
from django.http import HttpResponseForbidden
from .models import Profile, BuyerProfileModel, SellerProfileModel

# Create your views here.
#Roles
ALLOWED_ROLE_CHOICES = ['buyer', 'individual_seller', 'gallery']

#signup view
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()

            #Assign role
            role = form.cleaned_data.get('role')
            if role not in ALLOWED_ROLE_CHOICES:
                return HttpResponseForbidden
            group, created = Group.objects.get_or_create(name=role)
            user.groups.add(group)

            Profile.objects.create(user=user, role=role)

            login(request, user)

            if role == 'buyer':
                return redirect('buyer_profile')
            else:
                return redirect('seller_profile')

    else:
        form = SignupForm()

    return render(request, template_name='user/signup.html', context={'form': form})

def buyer_profile(request):
    profile = request.user.profile

    buyer_profile_obj, created = BuyerProfileModel.objects.get_or_create(profile=profile)

    if request.method == 'POST':
        form = BuyerProfileForm(request.POST, instance=buyer_profile_obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('buyer_profile')

    return render(request, template_name='user/buyer_profile.html', context={
        'form': BuyerProfileForm(instance=buyer_profile_obj),
    })

def seller_profile(request):

    profile = request.user.profile

    seller_profile_obj, created = SellerProfileModel.objects.get_or_create(profile=profile)

    if request.method == 'POST':
        form = SellerProfileForm(request.POST, instance=seller_profile_obj)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('seller_profile')

    return render(request, template_name='user/seller_profile.html', context={
        'form': SellerProfileForm(instance=seller_profile_obj),
    })

