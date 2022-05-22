import feedparser
from django.db import IntegrityError
from serials.models import Serial
import logging
import os

from .tasks import process_user_stats


def parse_serials():
    logging.warning("It is time to start the dramatiq task serials")
    feed_data = feedparser.parse("http://seasonvar.ru/rss.php")
    for z in feed_data["entries"]:
        if "сезон полностью" in z["title"].split(" серия")[0].split(",")[-1].lstrip():
            ep = "сезон полностью"
            try:
                new_serial = Serial.objects.create(
                    title=z["title"].split(",")[0].split("(")[0].rstrip(),
                    img=z["link"].split("-")[1],
                    serial_and_season="".join(z["title"].split(",")[:-1]),
                    episode=ep,
                )
                new_serial.save()
            except IntegrityError:
                pass
            finally:
                process_user_stats.send()
        else:
            ep = z["title"].split(" серия")[0].split(",")[-1].lstrip()
            try:
                obj, created = Serial.objects.update_or_create(
                    title=z["title"].split(",")[0].split("(")[0].rstrip(),
                    defaults={
                        "img": z["link"].split("-")[1],
                        "serial_and_season": "".join(z["title"].split(",")[:-1]),
                        "episode": ep,
                    },
                )

            except IntegrityError:
                pass
            finally:
                process_user_stats.send()
