from django.db import IntegrityError
from hh.models import Hh
import logging
import os
import requests
import json
import sys

from .tasks import process_user_stats


def hh_parse():
    logging.warning("It is time to start the dramatiq task HeadHunter")

    url = "https://api.hh.ru/vacancies?clusters=true&enable_snippets=true&st=searchVacancy&only_with_salary=true&specialization=1.221&per_page=100&area=1"
    try:
        html_text = requests.get(url).text
        data = json.loads(html_text)
        total_pages = data["pages"]
    except:
        sys.exit(2)  # НЕ ЗНАЮ ЧТО ЭТА ЗА ХУИТА

    for page in range(total_pages):
        try:
            current_data = json.loads(requests.get(f"{url}&page={page}").text)
        except:
            continue
        for item in current_data["items"]:
            if item["salary"]["from"] is None:
                item["salary"]["from"] = 0
            if item["salary"]["to"] is None:
                item["salary"]["to"] = 0
            if item["schedule"]["id"].lower() == "remote":
                if any(i in ["python", "django"] for i in item["name"].lower().split()):
                    try:
                        new_hh = Hh.objects.create(
                            name=item["name"].lower(),
                            salary=json.dumps(
                                {
                                    "to": item["salary"]["to"],
                                    "from": item["salary"]["from"],
                                    "currency": item["salary"]["currency"],
                                }
                            ),
                            url_id=item["alternate_url"].split("/")[-1],
                            published=item["published_at"],
                            requirement=item["snippet"]["requirement"],
                        )
                        new_hh.save()
                    except IntegrityError:
                        pass
                    finally:
                        process_user_stats.send()
