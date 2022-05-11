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
    hh_api = 'https://api.hh.ru/vacancies'
    hh_params = {
    'st':              'searchVacancy',
    'area':            '1'
    'cluster':         'true',
    'per_page':        '100',
    'specialization':  '1.221',
    'enable_snippets': 'true',
    'only_with_salary':'true',
    }
    if (html_text := requests.get(hh_api,params=hh_params)).status_code == requests.codes.ok:
        data = json.loads(html_text)
        total_pages = data["pages"]
    else:
        sys.exit(2)
    #    params_lists = {
    #            "jobs": ['''"разработчик", "тестировщик", "программист", "инженер", "devops", "аналитик", "администратор"'''],
    #            "lang": ["python", "django"],
    #            }
    #    schedule_params_list = {
    #            "schedule": ["remote"],
    #            }
    #
    filter_data = {}
    words_searching = 'python django'.split()
    for page in range(total_pages):
        hh_params['page'] = page
        if (response_test := requests.get(url,params=hh_params).status_code).status_code == requests.codes.ok:
            current_data = response_test.json()

        for item in current_data["items"]:
            
            if item["salary"]["from"] is None:
                item["salary"]["from"] = 0
            
            if item["salary"]["to"] is None:
                item["salary"]["to"] = 0
            
            if item["schedule"]["id"].lower() == "remote":
                if any(i in words_searching for i in item["name"].lower().split()):
                    # if "python" or "django" in item["name"].lower().split(' '):
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


#                filter_data.update({
#                    item["id"]: {
#                        "name": item["name"].lower(),
#                        "salary": {
#                            "to": item["salary"]["to"],
#                            "from": item["salary"]["from"],
#                            "currency": item["salary"]["currency"]
#                                },
#                        "url": item["alternate_url"].split('/')[-1],
#                        "schedule": item["schedule"]["id"].lower(),
#                        "published": item["published_at"],
#                        "requirement": item["snippet"]["requirement"]
#                        }
#                    })
#        print(filter_data)
#
#    prometheus_data = []
#    for fdt in filter_data:
#        dt = filter_data[fdt]
#        for param in params_lists:
#            for i in params_lists[param]:
#                try:
#                    salary_env = dt["salary"]["to"]
#                    salary = "to"
#                    if salary_env == 0:
#                        salary_env = dt["salary"]["from"]
#                        salary = "from"
#                    published, schedule, currency, url = dt['published'], dt['schedule'], dt["salary"]["currency"], dt['url']
#                    if i in dt["name"]:
#                        prometheus_data.append(dict(
#                                    name=i,
#                                    url=url,
#                                    currency=currency,
#                                    salary=salary,
#                                    schedule=schedule,
#                                    published=published,
#                                    salary_env=salary_env
#                                    ))
#                except: continue
#    prometheus_data.append(dict(job_total = data['found']))
#    print(prometheus_data)
#
