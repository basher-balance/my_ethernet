from django.db import IntegrityError
from anime.models import Anime, ListAnime
import logging
import asyncio
import httpx

from bs4 import BeautifulSoup
from .tasks import process_user_stats


data = list(ListAnime.objects.values('title'))
list_anime = [k['title'] for k in data]
list_a = [k['title'] for k in data]
url_base = "https://naruto-base.su"
link = f"{url_base}/novosti/drugoe_anime_ru"
# Количество страниц, которое будет просматривать код
pages = 4


async def get_html(client, url):
        response = await client.get(url)
        return response.text


async def get_name_and_id_anime():
    async with httpx.AsyncClient() as client:
        tasks = (
                get_html(
                    client, f'{link}?page{page}') for page in range(1, pages)
                )
        list_content = await asyncio.gather(*tasks)
        list_url_anime = []
        for content in list_content:
            soup = BeautifulSoup(content, "lxml")
            tags_h2 = soup.find_all('h2')
            for tag_h2 in tags_h2:
                tag_title = tag_h2.get_text()
                tag_href = tag_h2.find('a').get('href')
                for anime in list_anime:
                    if anime in tag_title:
                        link_to_anime = f'{url_base}{tag_href}'
                        list_url_anime.append(link_to_anime)
                        list_anime.remove(anime)

        tasks_two = (get_html(client, link) for link in list_url_anime)
        list_content_anime = await asyncio.gather(*tasks_two)

        return list_content_anime

list_anime_text = asyncio.run(get_name_and_id_anime())


def parse_content_anime():
    for content_anime in list_anime_text:
        soup = BeautifulSoup(content_anime, 'lxml')
        name_anime = soup.find('h1', attrs={'itemprop':'name'}).get_text()
        try:
            id_video = str(soup.find('a', id='ep6')).split("'")[1]
        except IndexError as e:
            print(f'аниме с сабами еще не вышло {e}')
        else:
            for a in list_a:
                if a in name_anime:
                    obj, created = Anime.objects.update_or_create(
                        id_anime=id_video,
                        defaults={
                            "title_anime": name_anime,
                            },
                        )
    for undetected_anime in list_anime:
        obj = ListAnime.objects.get(
            title=undetected_anime,
        )
        obj.delete()


def last_series_anime():
    logging.warning("It is time to start the dramatiq task anime")
    parse_content_anime()
    process_user_stats.send()
