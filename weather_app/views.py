# Create your views here.
from django.contrib.auth.views import LoginView
from .data import WeatherWrapper
from django.db import models
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *



class RegisterUser(CreateView):
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('weather_request')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Register"
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'login.html'

    def form_valid(self, form):
        # Отримання даних користувача з форми
        # Зберігаємо користувача у сесії після успішної аутентифікації
        self.request.session['user_pr_id'] = self.request.user.id
        return super().form_valid(form)

    def get_success_url(self):
        # Перевіряємо чи користувач вже зареєстрований
        if hasattr(self.request.user, 'profile'):
            # Якщо профіль існує, перенаправляємо на сторінку weather_request
            return reverse('weather_request')
        else:
            # Якщо профілю немає, перенаправляємо на сторінку index
            return reverse('index')

    def get_success_url(self):
        # Перенаправлення після успішного логіну
        return reverse('weather_request')


def index(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)

            # Отримання значень з об'єкта profile
            username = profile.username
            email = profile.email

            # Створення або отримання користувача
            user_profile, created = User.objects.get_or_create(username=username, email=email)
            if not created:
                user_profile.email = profile.email
                user_profile.save()

            # Зберігання ID користувача в сесії
            request.session['user_pr_id'] = user_profile.id
            return redirect('weather_request')

    else:
        form = UserRegisterForm()

    return render(request, 'index.html', {'form': form})


def weather_request(request):
    if request.method == 'GET':
        form = WeatherRequestForm(request.GET)
        if form.is_valid():
            city = form.cleaned_data['location']
            weather_data = WeatherWrapper(city)
            temperature = weather_data.get_temperature()
            description = weather_data.get_weather()

            response_data = {
                'temperature': temperature,
                'feels_like': weather_data.get_temp_feel(),
                'weather': description,
                'humidity': weather_data.get_humidity(),
                'visibility': weather_data.get_visibility(),
                'wind_speed': weather_data.get_wind(),
                'wind_direction': weather_data.get_wind_direct(),
                'city': city,
            }

            user_pr = request.session.get('user_pr_id')
            print("User profile ID from session:", user_pr)  # Відлагодження

            if not user_pr:
                print("User profile ID not found in session.")  # Відлагодження
                return redirect('register')

            try:
                profile = User.objects.get(id=user_pr)
                print("User profile found:", profile)  # Відлагодження
            except User.DoesNotExist:
                print("User does not exist in the database.")  # Відлагодження
                return redirect('register')

            weather_request = form.save(commit=False)
            weather_request.user_pr = profile
            weather_request.response_data = str(response_data)
            weather_request.save()

            # Зберігання даних в SearchHistory
            SearchHistory.objects.create(
                user=request.user,
                city=city,
                temperature=temperature,
                description=description
            )

            return render(request, 'weather_result.html', response_data)
        else:
            print("Form is not valid:", form.errors)

    else:
        form = WeatherRequestForm()
    return render(request, 'weather_form.html', {'form': form})


# @login_required
def history_view(request):
    user = request.user
    search_history = SearchHistory.objects.filter(user=user).order_by(
        '-search_date')

    context = {
        'search_history': search_history,
    }

    return render(request, 'history.html', context)
