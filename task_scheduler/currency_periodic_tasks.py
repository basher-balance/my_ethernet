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
    api_currency    = 'https://free.currconv.com/api/v7/convert'
    currency_params = {
        'q':'RUB_KZT',
        'compact':'ultra',
        'apiKey':appid_0
        }
    delete_currency.delete()
    currencies = {"RUB_KZT": "", "EUR_KZT": "", "USD_KZT": ""}
    if (r.get(api_currency,parmas=currency_params).status_code == re.codes.ok):
        for currency in currencies:
            currency_params['q'] = currency
            req = r.get(api_currency,params=currency_params).json()
            for k, v in req.items():
                currencies[k] = v
    else:
        for k in currencies:
            currencies[k] = "сервис free.currconv.com в данный момент не доступен"
    Currency.objects.create(currency=currencies)
    process_user_stats.send()

