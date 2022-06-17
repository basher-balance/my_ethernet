from celery import shared_task
from currencies.models import Currency
import requests
import os

CURCONV_TOKEN = os.environ.get("CURCONV_TOKEN")

@shared_task
def currencies_task():
    if CURCONV_TOKEN == None:
        return

    delete_currency = Currency.objects.all()
    delete_currency.delete()

    curconv_token = os.environ.get("CURCONV_TOKEN")
    currencies = {
        "RUB_KZT": "",
        "EUR_KZT": "",
        "USD_KZT": "",
    }

    for currency in currencies:
        url = f"https://free.currconv.com/api/v7/convert?q={currency}&compact=ultra&apiKey={curconv_token}"
        response = requests.get(url)

        if (response.status_code == 200):
            currencies[currency] = response.json()[currency]
        else:
            currencies[currency] = "Cервис currconv.com в данный момент не доступен"

    Currency.objects.create(currency=currencies)
