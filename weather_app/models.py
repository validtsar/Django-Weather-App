from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
import requests

class WeatherRequest(models.Model):
    user_pr = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weather_request')
    location = models.CharField(max_length=100)
    request_data = models.DateTimeField(auto_now_add=True)
    response_data = models.TextField()


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    description = models.CharField(max_length=255)
    search_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} - {self.user.username}"

