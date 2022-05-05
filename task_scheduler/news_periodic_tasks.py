from django.db import IntegrityError
from news.models import New
import logging
import os

from .tasks import process_user_stats


import requests
from bs4 import BeautifulSoup


def parse_news():
    logging.warning('It is time to start the dramatiq task news')
    '''Функция заносящая данные в базу данных и которую нужно будет вынести'''
    url = "https://mail.ru/"
    r_text = requests.get(url).text
    soup = BeautifulSoup(r_text, 'lxml')
# Ищу загаловок главной новости
    find_title_tags = soup.findAll('a', class_='news__list__item__link')
    list_ftg = list(find_title_tags) 
# Загружаю главную новость майл ру в базу если такой новости еще нет
    try:
        general_new = New.objects.create(news=list_ftg[1].get_text(), link_news=list_ftg[0]['href'])
        general_new.save(force_update=True)
    except IntegrityError:
       pass
    finally:
        # Ищу обычные новости на стартовой странице майл ру
        find_tags = soup.findAll('a', class_='news__list__item__link news__list__item__link_simple')
        for find_tag in find_tags:
            # Загружаю их в базу если таких нет
            try:
                news_text_and_link = New.objects.create(news=find_tag.find(class_="news__list__item__link__text").get_text(), link_news=find_tag['href'])
            except IntegrityError:
                pass
            else:
                news_text_and_link.save(force_update=True)
    process_user_stats.send()
