from django.db import models


class Youtube_model(models.Model):
    iframe = models.CharField('Айфрейм', max_length=300, unique=True)
    _is_expired = models.BooleanField(default=False)

    def hidden(pk):
        r = Youtube_model.objects.get(pk=pk)
        r._is_expired = True
        r.save()
