from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
import requests

class Profile(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    city = models.CharField(max_length=100)

class WeatherRequest(models.Model):
    user_pr = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='weather_request')
    location = models.CharField(max_length=100)
    request_data = models.DateTimeField(auto_now_add=True)
    response_data = models.TextField()



