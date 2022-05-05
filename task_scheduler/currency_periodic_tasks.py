from django.db import IntegrityError
from currencies.models import Currency
import logging
import os
import requests as r

from .keys import appid_0

from .tasks import process_user_stats


def currency_parse():
    logging.warning("It is time to start the dramatiq task currecncy")
    delete_currency = Currency.objects.all()
    delete_currency.delete()
    currencies = {"RUB_KZT": "", "EUR_KZT": "", "USD_KZT": ""}
    if (
        r.get(
            "https://free.currconv.com/api/v7/convert?q=RUB_KZT&compact=ultra&apiKey="
            + appid_0
        ).status_code
        == 200
    ):
        for currency in currencies:
            url = f"https://free.currconv.com/api/v7/convert?q={currency}&compact=ultra&apiKey={appid_0}"
            req = r.get(url).json()
            for k, v in req.items():
                currencies[k] = v
    else:
        for k in currencies:
            currencies[k] = "сервис free.currconv.com в данный момент не доступен"
    Currency.objects.create(currency=currencies)
    process_user_stats.send()
