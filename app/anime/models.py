from django.db import models


class Anime(models.Model):
    """Модель аниме"""

    title_anime = models.CharField("Название и серия")
    id_anime = models.PositiveIntegerField(
        "ID видео для портала sibnet",
        unique=True
    )
    date_added = models.DateTimeField(auto_now_add=True)
    _is_expired = models.BooleanField(default=False)

    def __str__(self):
        return self.title_anime

    def hidden(pk):
        r = Anime.objects.get(pk=pk)
        r._is_expired = True
        r.save()


class ListAnime(models.Model):
    '''Список анимe в БД, который будет парситься'''
    title = models.CharField("Название", unique=True)

    def __str__(self):
        return self.title
