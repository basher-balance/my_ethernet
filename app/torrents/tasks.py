from celery import shared_task
from torrents.models import Torrent, ListSerials
import feedparser


@shared_task
def torrents_task():
    data_in_bd = list(ListSerials.objects.values('title'))
    list_serials = [k['title'] for k in data_in_bd]
    data_rss = feedparser.parse("http://rutor.is/rss.php?category=4")

    for serial in list_serials:
        for i in range(len(data_rss["entries"])):
            title_entries = data_rss["entries"][i]["title"]
            if serial in title_entries:
                Torrent.objects.update_or_create(
                    title=data_rss["entries"][i]["title"],
                    defaults={
                        "link": data_rss["entries"][i]["link"].split("/")[-1],
                        # "published": data_rss["entries"][i]["published"],
                    },
                )
