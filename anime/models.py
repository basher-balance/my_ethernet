from django.db import models


class Anime(models.Model):
    """Модель аниме"""

    title_anime = models.CharField("Название и серия", max_length=50)
    link_anime = models.URLField("Ссылка на anime", unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    _is_expired = models.BooleanField(default=False)

    def hidden(pk):
        r = Anime.objects.get(pk=pk)
        r._is_expired = True
        r.save()
