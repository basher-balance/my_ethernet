import requests
import logging
import os

from currencies.models import Currency
from .tasks import process_user_stats


def currency_parse():
    logging.warning("It is time to start the dramatiq task currency")

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
    process_user_stats.send()
