from .models import WeatherRequest
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class WeatherRequestForm(forms.ModelForm):
    class Meta:
        model = WeatherRequest
        fields = ['location']


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
