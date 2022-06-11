from django.db import models


class Currency(models.Model):
    """Модель валюты"""
    currency = models.JSONField("Валюта")
    
    def __str__(self):
        return self.currency
