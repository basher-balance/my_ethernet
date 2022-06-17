from django.shortcuts import render, redirect
from .models import Currency


def currency_parse(request):
    """Выводит данные из модели Currency"""
    currency_last = list(Currency.objects.values())
    return render(
        request,
        "currency.html",
        {"currency_last": currency_last[0]["currency"]},
    )
