from django.db import models


class Currency(models.Model):
    """Модель валюты"""

    currency = models.JSONField("Валюта")
