# Generated by Django 5.0.6 on 2024-08-18 11:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_app', '0002_searchhistory'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='weatherrequest',
            name='user_pr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weather_request', to=settings.AUTH_USER_MODEL),
        ),
    ]
