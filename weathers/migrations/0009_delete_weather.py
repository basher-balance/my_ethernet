# Generated by Django 4.0.3 on 2022-05-12 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weathers', '0008_delete_weather_today_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Weather',
        ),
    ]
