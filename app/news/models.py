from django.db import models


class New(models.Model):
    """Новости с mail.ru"""

    news = models.TextField("Новость", unique=True)
    link_news = models.URLField("Ссылка на новость")
    date_added = models.DateTimeField(auto_now_add=True)
    _is_expired = models.BooleanField(default=False)

    def __str__(self):
        return self.news

    def hidden(pk):
        r = New.objects.get(pk=pk)
        r._is_expired = True
        r.save()
