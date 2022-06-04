from django.db import IntegrityError
from hh.models import Hh
from .tasks import process_user_stats
import httpx
import asyncio
import requests
import logging
import json
 
api_hh = 'https://api.hh.ru/vacancies'
 
params = dict(
    only_with_salary='true',
    enable_snippets='true',
    specialization=1.221,   
    per_page=100,
    clusters='true',
    area=1,
    st='searchVacancy',
    )
 
clear_hh = {
    'items': []
}
 
async def parse_hh(client,page):
    response = await client.get(f'{api_hh}?page={page}',params=params)
    return response.json()
async def filter_hh(json_hh):
    for item in json_hh['items']:
        if item["schedule"]["id"].lower() != 'remote':continue
        if any(i in item['name'].lower() for i in ('python','django')):
            if not item['salary']['from']:
                item['salary']['from'] = 0
            if not item['salary']['to']:
                item['salary']['to']   = 0
            clear_hh['items'].append(item)
 
async def main():
    total_pages = requests.get(api_hh,params=params).json()['pages']
    async with httpx.AsyncClient() as client:
        tasks        = [parse_hh(client,i) for i in range(total_pages)]
        for i in asyncio.as_completed(tasks):
            await filter_hh(await i)
        # jsons_list   = await asyncio.gather(*tasks)
        # tasks_filter = (filter_hh(json_file) for json_file in jsons_list)
        # await asyncio.gather(*tasks_filter)
        
#        create_object()
        #print(jsons_list[0]['items'][0]['salary'])
        #print(jsons_list)
#start = time.time()
#print(clear_hh)
#print(len(clear_hh['items']))
#print(time.time()-start)

def create_object():
    logging.warning("It is time to start the dramatiq task HeadHunter")
    asyncio.run(main())
    for item in clear_hh['items']:
        try:
            new_hh = Hh.objects.create(
                name=item["name"].lower(),
                salary=json.dumps(
                    {
                        "to":       item["salary"]["to"],
                        "from":     item["salary"]["from"],
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
