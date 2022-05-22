from django.db import models


class News(models.Model):
    """Новости с mail.ru"""

    news = models.TextField("Новость", max_length=200, unique=True)
    link_news = models.URLField("Ссылка на новость")
    date_added = models.DateTimeField(auto_now_add=True)
    _is_expired = models.BooleanField(default=False)

    def hidden(pk):
        r = News.objects.get(pk=pk)
        r._is_expired = True
        r.save()
