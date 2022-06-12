import requests
import logging
import os

from django.db import IntegrityError
from vk.models import Vk
from datetime import datetime
from operator import itemgetter
from .tasks import process_user_stats


def posts_vk_group():
    logging.warning("It is time to start the dramatiq task vk")
    link = "https://api.vk.com/method/"
    method = "wall.get"
    access_token = os.environ.get("VK_ACCESS_TOKEN")
    owner_id = os.environ.get("VK_OWNER_ID")
    response = requests.get(
        link + method,
        params={
            "v": 5.131,
            "access_token": access_token,
            "owner_id": owner_id,
            "domain": None,
            "count": 100,
        },
    )
    responses = response.json()["response"]["items"]
    sorted_responses = sorted(
        responses,
        reverse=True,
        key=itemgetter("date"),
    )
    for response in sorted_responses:
        try:
            text = response['text']
            link = text.split(': http://')[1].split('/n')[0]
            link_post = f"http://{link}"
        except IndexError:
            link_post = "http://habr.com"
        try:
            link_image_post = response["attachments"][0]["photo"]["sizes"][-1][
                "url"
            ]
        except KeyError:
            link_image_post = "No image"
        try:
            vk_published_post = Vk.objects.create(
                data_post=datetime.fromtimestamp(response["date"]).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                text_post=response["text"],
                link_post=link_post,
                link_image_post=link_image_post,
            )
        except IntegrityError:
            pass
        else:
            vk_published_post.save(force_update=True)
    process_user_stats.send()
