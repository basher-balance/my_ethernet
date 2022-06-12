from django.db import models


class Twitch_model(models.Model):
    streamer = models.CharField("Канал твича", unique=True)
