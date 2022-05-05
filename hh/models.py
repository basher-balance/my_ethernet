from django.db import models


class Hh(models.Model):
    name = models.CharField("Название вакансии", max_length=45)
    salary = models.JSONField("Информация по оплате")
    url_id = models.PositiveIntegerField("ID https://hh.ru/vacancy/...", unique=True)
    published = models.CharField("Дата", max_length=20)
    requirement = models.CharField("Подробности", max_length=150)
    _is_expired = models.BooleanField(default=False)

    def hidden(pk):
        r = Hh.objects.get(pk=pk)
        r._is_expired = True
        r.save()
