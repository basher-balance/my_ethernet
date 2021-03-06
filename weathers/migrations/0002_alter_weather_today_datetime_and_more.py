# Generated by Django 4.0.3 on 2022-04-02 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("weathers", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="weather_today",
            name="datetime",
            field=models.DateField(verbose_name="Дата"),
        ),
        migrations.AlterField(
            model_name="weather_today",
            name="sunrise",
            field=models.DateField(verbose_name="Восход"),
        ),
        migrations.AlterField(
            model_name="weather_today",
            name="sunset",
            field=models.DateField(verbose_name="Закат"),
        ),
    ]
