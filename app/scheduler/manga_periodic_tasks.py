from django.db import IntegrityError
from manga.models import Manga
import logging
import os
import httpx
from bs4 import BeautifulSoup

# import re


from .tasks import process_user_stats


def manga_parse():
    logging.warning("It is time to start the dramatiq task manga")
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
            name="onepanchman", link=link_onepunch)
    except IntegrityError:
        pass
    else:
        manga_create.save(force_update=True)
    process_user_stats.send()


# Можно использовать альтернативный сайт, у которого есть API
# https://api.remanga.org/api/titles/chapters/?branch_id=48&count=1&ordering=-index&page=1&user_data=1
#    url = "https://mangalib.me/onepunchman?section=info"
#    # Получаю ссылку на последнюю главу манги "Ванпанчмен"
#    r_http = httpx.Client(http2=True)
#    response_http = r_http.get(url)
#    src = response_http.text
#    soup_http = BeautifulSoup(src, 'lxml')
#    ads = str(soup_http.find("script"))
#    try:
#        chapter_volume = eval('{{{}}}'.format(re.findall(r'"chapter_volume":\w+', ads)[0]))
#        chapter_number = eval('{{{}}}'.format(re.findall(r'"chapter_number":"\w+"', ads)[0]))
