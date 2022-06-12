from django.core.management.base import BaseCommand, CommandError
from apscheduler.schedulers.background import BlockingScheduler
import pytz

from apscheduler.triggers.interval import IntervalTrigger

from scheduler.news_periodic_tasks import parse_news
from scheduler.currency_periodic_tasks import currency_parse
from scheduler.manga_periodic_tasks import manga_parse
from scheduler.vk_periodic_tasks import posts_vk_group
from scheduler.anime_periodic_tasks import last_series_anime
from scheduler.twitch_periodic_tasks import twitch_parse
from scheduler.youtube_periodic_tasks import youtube_parse
from scheduler.serials_periodic_tasks import parse_serials
from scheduler.torrents_periodic_tasks import torrents_parse
from scheduler.hh_periodic_tasks import create_object


class Command(BaseCommand):
    help = "Run blocking scheduler to create periodical tasks"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Preparing scheduler"))
        scheduler = BlockingScheduler(timezone=pytz.UTC)
        # Запускаю функции парсинга при запуске планировщика
        create_object()
        torrents_parse()
        parse_serials()
        youtube_parse()
        twitch_parse()
        posts_vk_group()
        parse_news()
        currency_parse()
        manga_parse()
        last_series_anime()
        # Создаю интервалы обновления
        time_update_hh= IntervalTrigger(minutes=180)
        time_update_torrents = IntervalTrigger(minutes=180)
        time_update_serials = IntervalTrigger(minutes=70)
        time_update_youtube = IntervalTrigger(minutes=80)
        time_update_twitch = IntervalTrigger(minutes=10)
        time_update_vk = IntervalTrigger(minutes=120)
        time_update_news = IntervalTrigger(minutes=60)
        time_update_currency = IntervalTrigger(minutes=60)
        time_update_manga = IntervalTrigger(minutes=120)
        time_update_anime= IntervalTrigger(minutes=120)

        # Добавляю в планировщик с установленными интервалами
        scheduler.add_job(create_object, time_update_hh)
        scheduler.add_job(torrents_parse, time_update_torrents)
        scheduler.add_job(parse_serials, time_update_serials)
        scheduler.add_job(youtube_parse, time_update_youtube)
        scheduler.add_job(twitch_parse, time_update_twitch)
        scheduler.add_job(last_series_anime, time_update_anime)
        scheduler.add_job(posts_vk_group, time_update_vk)
        scheduler.add_job(manga_parse, time_update_manga)
        scheduler.add_job(parse_news, time_update_news)
        scheduler.add_job(currency_parse, time_update_currency)
        self.stdout.write(self.style.NOTICE("Start scheduler"))
        scheduler.start()
