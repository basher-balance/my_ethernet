from django.db import models


class Serial(models.Model):
    title = models.CharField("Название сериала", max_length=100, unique=True)
    img = models.PositiveIntegerField("ID картинки сериала")
    serial_and_season = models.CharField("Название сериала и сезона", max_length=100)
    episode = models.CharField("Количество серий либо сезон полностью", max_length=20)
    data = models.DateTimeField(
        "Автоматически созданная дата после загрузки элемента базы", auto_now_add=True
    )
    _is_expired = models.BooleanField(default=False)

    def hidden(pk):
        r = Serial.objects.get(pk=pk)
        r._is_expired = True
        r.save()


#
#
# Молодой Скала (2 сезон), 7 серия (RuDub)
# Лучший пекарь Британии (6 сезон), сезон полностью
# Зачарованные (2018) (4 сезон), 8 серия
# Легенда, 21 серия (RuDub)
# Нереалити, 5 серия
# Человек, упавший на Землю, 1 серия (LostFilm)
