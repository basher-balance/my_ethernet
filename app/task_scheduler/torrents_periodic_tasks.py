import feedparser
import logging

from .tasks import process_user_stats
from torrents.models import Torrent, ListSerials


def torrents_parse():
    logging.warning("It is time to start the dramatiq task torrents")
    data_in_bd = list(ListSerials.objects.values('title'))
    list_serials = [k['title'] for k in data_in_bd]
    data_rss = feedparser.parse("http://rutor.is/rss.php?category=4")
    for serial in list_serials:
        for i in range(len(data_rss["entries"])):
            title_entries = data_rss["entries"][i]["title"]
            if serial in title_entries:
                new_torrent, created = Torrent.objects.update_or_create(
                    title=data_rss["entries"][i]["title"],
                    defaults = {
                        "link": data_rss["entries"][i]["link"].split("/")[-1],
                        #                        "published": data_rss["entries"][i]["published"],
                        },
                    )
    process_user_stats.send()
