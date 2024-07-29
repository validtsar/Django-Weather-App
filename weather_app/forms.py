from django import forms
from .models import WeatherRequest, Profile
from django.contrib.auth.forms import AuthenticationForm

class WeatherRequestForm(forms.ModelForm):
    class Meta:
        model = WeatherRequest
        fields = ['location']

class Profile_form(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['name', 'city']


