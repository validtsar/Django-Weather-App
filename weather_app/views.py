
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import requests

# Create your views here.

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import WeatherRequest, Profile
from .forms import WeatherRequestForm, Profile_form
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib import messages
from .data import WeatherWrapper
from django.contrib.auth import authenticate, login
from django.db import models


def index(request):
    if request.method == 'POST':
        form = Profile_form(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)

            # Отримання значень з об'єкта profile
            name = profile.name
            city = profile.city


            try:
                user_profile, created = Profile.objects.get_or_create(name=name, city=city)
                if not created:
                    user_profile.city = profile.city
                    user_profile.save()
                    messages.info(request, 'The user already exists.')
                request.session['user_pr_id'] = user_profile.id
                return redirect('weather_request')
            except MultipleObjectsReturned:
                user_profiles = Profile.objects.filter(name=name, city=city)
                user_profile = user_profiles.first()
                request.session['user_pr_id'] = user_profile.id
                messages.warning(request, 'Multiple profiles found. Using the first one.')
                return redirect('weather_request')
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')
                return render(request, 'index.html', {'form': form})
    else:
        form = Profile_form()
    return render(request, 'index.html', {'form': form})


def weather_request(request):
    if request.method == 'GET':
        form = WeatherRequestForm(request.GET)
        if form.is_valid():
            city = form.cleaned_data['location']
            weather_data = WeatherWrapper(city)
            response_data = {
                'temperature': weather_data.get_temperature(),
                'feels_like': weather_data.get_temp_feel(),
                'weather': weather_data.get_weather(),
                'humidity': weather_data.get_humidity(),
                'visibility': weather_data.get_visibility(),
                'wind_speed': weather_data.get_wind(),
                'wind_direction': weather_data.get_wind_direct(),
                'city': city,
            }
            user_pr = request.session.get('user_pr_id')
            if not user_pr:
                return redirect('index')

            profile = Profile.objects.get(id=user_pr)
            weather_request = form.save(commit=False)
            weather_request.user_pr = profile
            weather_request.response_data = str(response_data)
            weather_request.save()

            return render(request, 'weather_result.html', response_data)

    else:
        form = WeatherRequestForm()
    return render(request, 'weather_form.html', {'form': form})

def profile_view(request):
    if request.method == 'POST':
        form = Profile_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('weather_request')
    else:
        form = Profile_form()
    return render(request, 'profile.html', {'form': form})
