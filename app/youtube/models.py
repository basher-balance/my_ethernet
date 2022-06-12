from django.db import models


class Youtube_model(models.Model):
    id_video = models.CharField("ИД Видео", max_length=15, unique=True)
    _is_expired = models.BooleanField(default=False)

    def hidden(pk):
        r = Youtube_model.objects.get(pk=pk)
        r._is_expired = True
        r.save()
