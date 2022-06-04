import feedparser
import logging

from .tasks import process_user_stats
from torrents.models import Torrent


serial = {
    "Детство Шелдона": "Кураж-Бамбей",
}


def torrents_parse():
    logging.warning("It is time to start the dramatiq task torrents")
    d = feedparser.parse("http://rutor.is/rss.php?category=4")
    for k, v in serial.items():
        for z in range(len(d["entries"])):
            title_entries = d["entries"][z]["title"]
            if k in title_entries and v in title_entries:
                new_torrent, created = Torrent.objects.update_or_create(
                    title=d["entries"][z]["title"],
                    defaults = {
                        "link": d["entries"][z]["link"].split("/")[-1],
                        "published": d["entries"][z]["published"],
                        },
                    )
    process_user_stats.send()
