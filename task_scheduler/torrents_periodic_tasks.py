import feedparser
from django.db import IntegrityError
from torrents.models import Torrent
import logging
import os

from .tasks import process_user_stats


serial = {
    'Детство Шелдона': 'Кураж-Бамбей',
}



def torrents_parse():
    logging.warning('It is time to start the dramatiq task torrents')
    d = feedparser.parse('http://rutor.is/rss.php?category=4')
    for k, v in serial.items():
        for z in range(len(d['entries'])):
            title_entries = d['entries'][z]['title']
            if k in title_entries and v in title_entries:
                try:
                    new_torrent = Torrent.objects.create(
                            title=d['entries'][z]['title'],
                            link=d['entries'][z]['link'].split('/')[-1],
                            published=d['entries'][z]['published']
                            )
                    new_torrent.save()
                except IntegrityError:
                    pass
                finally:
                    process_user_stats.send()
