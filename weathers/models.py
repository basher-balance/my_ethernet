from django.db import models


class Weather(models.Model):
    '''Погода и визуализация погоды'''
    weather_daily = models.JSONField('Данные на неделю')
    #diagram = models.TextField('Тег диаграммы')


class Weather_Today(models.Model):
    cloud = models.PositiveSmallIntegerField('Облачность')
    datetime = models.CharField('Дата', max_length=20)
    humidity = models.PositiveSmallIntegerField('Влажность')
    moon_phase = models.FloatField('Фаза луны')
    pup = models.PositiveSmallIntegerField('Вероятность влаги')
    pressure = models.PositiveSmallIntegerField('Давление')
    #rain = models.FloatField('Дождь')
    #snow = models.FloatField('Снег')
    sunrise = models.CharField('Восход', max_length=20)
    sunset = models.CharField('Закат', max_length=20)
    temp = models.JSONField('Температура')
    uvi = models.FloatField('Ультрафиолетовый индекс')
    weather_description = models.CharField('Состояние погоды', max_length=20)
    weather_icon = models.CharField('Иконка погоды', max_length=6)
    weather_main = models.CharField('Группа погодных параметров', max_length=10)
