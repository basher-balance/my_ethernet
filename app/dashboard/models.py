from django.db import models


class Dashboard(models.Model):
    '''Модель информационной панели'''
    title_undetected_anime = models.CharField(
        "Название аниме",
        max_length=128,
        unique=True,
    )
    date_added = models.DateTimeField(
        "Дата обнаружения необнаруженного аниме",
        auto_now_add=True,
    )

    def delete_from_anime_parse_list(k):
        r = Dashboard.objects.get(title_undetected_anime=k)
        r.delete()
