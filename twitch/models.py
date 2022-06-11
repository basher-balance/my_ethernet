from django.db import models


class Twitch_model(models.Model):
    streamer = models.CharField("Канал твича", max_length=30, unique=True)


    def __str__(self):
        return self.streamer
