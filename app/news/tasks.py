from celery import shared_task
from news.models import New
from bs4 import BeautifulSoup
import requests


@shared_task
def news_task():
    url = "https://mail.ru/"
    r_text = requests.get(url).text
    soup = BeautifulSoup(r_text, "lxml")

    # Ищу загаловок главной новости
    find_title_tags = soup.findAll("a", class_="news__list__item__link")
    list_ftg = list(find_title_tags)

    # Загружаю главную новость майл ру в базу если такой новости еще нет
    New.objects.update_or_create(
        news=list_ftg[1].get_text(),
        defaults={
            "link_news": list_ftg[0]["href"],
        },
    )

    # Ищу обычные новости на стартовой странице майл ру
    find_tags = soup.findAll(
        "a",
        class_="news__list__item__link news__list__item__link_simple",
    )

    for find_tag in find_tags:
        # Загружаю их в базу если таких нет
        New.objects.update_or_create(
            news=find_tag.find(
                class_="news__list__item__link__text"
            ).get_text(),
            defaults={
                "link_news": find_tag["href"],
            },
        )
