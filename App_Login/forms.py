from django import forms
from django.forms import ModelForm
from .models import User, Profile
from django.contrib.auth.forms import UserCreationForm


class ProfileFrom(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)


class SignUpFrom(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)