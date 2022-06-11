from django.db import models


class Torrent(models.Model):
    title = models.CharField("Название сериала", max_length=50)
    link = models.PositiveIntegerField("ID на ссылку торрента", unique=True)
    published = models.DateTimeField(
        "Автоматически созданная дата после загрузки элемента базы", auto_now_add=True
    )
    _is_expired = models.BooleanField(default=False)


    def __str__(self):
        return self.title


class ListSerials(models.Model):
    '''Список сериалов в БД, который будет парситься'''
    title = models.CharField("Название", max_length=50, unique=True)
    
    def __str__(self):
        return self.title
