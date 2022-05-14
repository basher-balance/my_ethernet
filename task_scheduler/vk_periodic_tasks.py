from django.db import IntegrityError
from vk.models import Vk

import requests
from datetime import datetime
from operator import itemgetter

import logging
import os
from .tasks import process_user_stats
from .keys import service_key_access_vk


def posts_vk_group():
    logging.warning("It is time to start the dramatiq task vk")
    link = "https://api.vk.com/method/"
    method = "wall.get"
    access_token = service_key_access_vk
    v = 5.131
    owner_id = -20629724
    domain = None
    count = 100
    response = requests.get(
        link + method,
        params={
            "access_token": access_token,
            "v": v,
            "owner_id": owner_id,
            "domain": domain,
            "count": count,
        },
    )
    all_respons = response.json()["response"]["items"]
    sorted_all_respons = sorted(all_respons, reverse=True, key=itemgetter("date"))
    for sorted_all_respon in sorted_all_respons:
        try:
<<<<<<< HEAD
            link_post = fr"http://{sorted_all_respon['text'].split(': http://')[1].split('/n')[0]}"
=======
             link_post = (
                "http://"
                + sorted_all_respon["text"].split(": http://")[1].split("\n")[0]
            )
>>>>>>> main
        except IndexError:
            link_post = "http://habr.com"
        try:
            link_image_post = sorted_all_respon["attachments"][0]["photo"]["sizes"][-1][
                "url"
            ]
        except KeyError:
            link_image_post = "No image"
        try:
            vk_published_post = Vk.objects.create(
                data_post=datetime.fromtimestamp(sorted_all_respon["date"]).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                text_post=sorted_all_respon["text"],
                link_post=link_post,
                link_image_post=link_image_post,
            )
        except IntegrityError:
            pass
        else:
            vk_published_post.save(force_update=True)
    process_user_stats.send()
