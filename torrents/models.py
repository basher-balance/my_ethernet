from django.db import models
 
 
class Torrent(models.Model):
    title = models.CharField("Название сериала", max_length=50)
    link = models.PositiveIntegerField("ID на ссылку торрента", unique=True)
    published = models.DateTimeField("Автоматически созданная дата после загрузки элемента базы", auto_now_add=True)
    _is_expired = models.BooleanField(default=False)
 
    def hidden(pk):
        r = Torrent.objects.get(pk=pk)
        r._is_expired = True
        r.save()
