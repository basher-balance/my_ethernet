from django.db import IntegrityError
from anime.models import Anime
import logging
import os
import asyncio
import httpx

from bs4 import BeautifulSoup
from .tasks import process_user_stats


list_anime = [
    "Семья шпиона",
    "Мир отомэ-игр — это тяжёлый мир для мобов",
    "Госпожа Кагуя: в любви как на войне",
    "Рыцарь-скелет вступает в параллельный мир",
    "Восхождение героя щита 2 сезон",
    "Перестану быть героем",
    #    "Тусовщик Кунмин",
    "Величайший Повелитель Демонов перерождается как",
]
url_base = "https://naruto-base.su"
link = f"{url_base}/novosti/drugoe_anime_ru"
# Количество страниц, которое будет просматривать код
pages = 3


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
        dict_name_id = {}
        for content_anime in list_content_anime:
            soup = BeautifulSoup(content_anime, 'lxml')
            name_anime = soup.find('h1', attrs={'itemprop':'name'}).string
            id_video = str(soup.find('a', id='ep6')).split("'")[1]
            dict_name_id[name_anime] = id_video
            try:
                anime_title_anime = Anime.objects.create(
                        title_anime=name_anime,
                        id_anime=id_video,
                    )
                anime_title_anime.save(force_update=True)
            except IntegrityError:
                pass


def last_series_anime():
    logging.warning("It is time to start the dramatiq task anime")
    asyncio.run(get_name_and_id_anime())
    process_user_stats.send()
