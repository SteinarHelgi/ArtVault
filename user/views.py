from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .forms import SignupForm
from django.http import HttpResponseForbidden

# Create your views here.
ALLOWED_ROLE_CHOICES = ['buyer', 'seller']
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()

            #Assign role
            role = form.cleaned_data.get('role')
            if role not in ALLOWED_ROLE_CHOICES:
                return HttpResponseForbidden
            group = Group.objects.get_or_create(name=role)
            user.groups.add(group)

            login(request, user)
            #ferð þar sem að þú býrð til profile
            return redirect('/')

    else:
        form = SignupForm()

    return render(request, template_name='user/signup.html', context={'form': form})