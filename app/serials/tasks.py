from celery import shared_task
from serials.models import Serial
import feedparser

@shared_task
def serials_task():
    feed_data = feedparser.parse("http://seasonvar.ru/rss.php")
    for entries in feed_data["entries"]:
        Serial.objects.update_or_create(
            title=entries["title"].split(",")[0].split("(")[0].rstrip(),
            defaults={
                "img": entries["link"].split("-")[1],
                "serial_and_season": "".join(entries["title"].split(",")[:-1]),
                "episode": entries["title"].split(" серия")[0].split(",")[-1].lstrip(),
            },
        )
