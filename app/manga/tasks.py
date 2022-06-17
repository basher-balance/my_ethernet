from celery import shared_task
from manga.models import Manga
from django.db import IntegrityError
from bs4 import BeautifulSoup
import httpx


@shared_task
def manga_task():
    url = "https://mangapoisk.ru/manga/vanpanchmen"
    # Получаю ссылку на последнюю главу манги "Ванпанчмен"
    r_http = httpx.Client(http2=True)
    response_http = r_http.get(url)
    src = response_http.text
    soup_http = BeautifulSoup(src, "lxml")
    tc = (
        soup_http.find_all("a", class_="btn btn-outline-primary")[1]
        .get("href")
        .split("/")[-1]
    )
    link_onepunch = f"https://mangapoisk.ru/manga/vanpanchmen/chapter/{tc}"
    try:
        manga_create = Manga.objects.create(
            name="onepanchman",
            link=link_onepunch,
        )
    except IntegrityError:
        pass
    else:
        manga_create.save(force_update=True)
