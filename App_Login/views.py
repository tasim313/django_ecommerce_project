from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Profile
from .forms import ProfileFrom, SignUpFrom
from django.contrib import messages

# Create your views here.


def sign_up(request):
    form = SignUpFrom()
    if request.method == 'POST':
        form = SignUpFrom(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created Successfully!')
            return HttpResponseRedirect(reverse('App_Login:login'))
    return render(request, 'App_Login/signup.html', context={'form': form})


def login_user(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('App_Shop:Home'))
    return render(request, 'App_Login/login.html', context={'form':form})


@login_required
def logout_user(request):
    logout(request)
    messages.warning(request, 'You are logged out !!')
    return HttpResponseRedirect(reverse('App_Shop:Home'))


@login_required
def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileFrom(instance=profile)
    if request.method == 'POST':
        form = ProfileFrom(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Changed Save !!')
            form = ProfileFrom(instance=profile)
    return render(request, 'App_Login/change_profile.html', context={'form': form})