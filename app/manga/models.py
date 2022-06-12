from django.db import models


class Manga(models.Model):
    """Манга"""
    name = models.CharField("Название аниме", max_length=128)
    link = models.URLField("Ссылка на аниме", unique=True)
    _is_expired = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def hidden(pk):
        r = Manga.objects.get(pk=pk)
        r._is_expired = True
        r.save()
