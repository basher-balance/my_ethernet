# Generated by Django 4.0.3 on 2022-06-12 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Youtube_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_video', models.CharField(max_length=16, unique=True, verbose_name='ID Видео')),
                ('_is_expired', models.BooleanField(default=False)),
            ],
        ),
    ]