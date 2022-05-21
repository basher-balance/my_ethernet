# Generated by Django 4.0.3 on 2022-05-20 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_anime', models.CharField(max_length=50, verbose_name='Название и серия')),
                ('id_anime', models.PositiveIntegerField(unique=True, verbose_name='ID видео для портала sibnet')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('_is_expired', models.BooleanField(default=False)),
            ],
        ),
    ]
