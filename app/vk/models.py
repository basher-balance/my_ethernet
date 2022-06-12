from django.db import models


class Vk(models.Model):
    """Модель вк"""

    data_post = models.CharField("Дата публикации", max_length=32)
    text_post = models.TextField("Заголовок поста")
    link_post = models.URLField("Ссылка на публикацию", unique=True)
    link_image_post = models.URLField("Ссылка на картинку")
    _is_expired = models.BooleanField(default=False)

    def hidden(pk):
        r = Vk.objects.get(pk=pk)
        r._is_expired = True
        r.save()
