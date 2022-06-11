import logging

from youtube.models import Youtube_model

from .tasks import process_user_stats
from .youtube_build import youtube

import asyncio
import httpx


def getSubs() -> dict:
    reqSubs = youtube.subscriptions().list(
        part="snippet,contentDetails", maxResults=100, mine=True
    )
    return reqSubs.execute()


def getChannel(channelId: str) -> dict:
    reqChannel = youtube.channels().list(
        part="contentDetails", id=channelId
    )
    return reqChannel.execute()


async def get_html(client, url):
        response = await client.get(url)
        return response.text


async def get_name_and_id_anime(list_channel_id: list):
    async with httpx.AsyncClient() as client:
        tasks = (
                get_html(
                    client, getChannel(channel)) for channel in list_channel_id
                )
        list_content = await asyncio.gather(*tasks)
        return list_content


def getPlaylistsItems(uploads: str) -> dict:
    req_playlistItems = youtube.playlistItems().list(
        part="contentDetails", playlistId=uploads, maxResults=1
    )
    return req_playlistItems.execute()


def getListChannelId(dictMySubs: dict) -> list:
    quantitySubs = range(dictMySubs['pageInfo']['totalResults'])
    list_ChannelId_MySubs = [
            dictMySubs["items"][mysab]["snippet"]["resourceId"]["channelId"] 
            for mysab in quantitySubs
            ]
    return list_ChannelId_MySubs


def getUploads(playlist_id: dict) -> str:
    return playlist_id["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]


def getVideoId(items: dict) -> str:
    return items["items"][0]["contentDetails"]["videoId"]


def createCellDB(video: str) -> None:
    fieldYoutubeModel, created = Youtube_model.objects.update_or_create(
            id_video=video
            )


# Получаю словарь по каналам, которые я отслеживаю
mySubs = getSubs()
# Получаю уникальные идентификаторы этих каналов
chanelIds = getListChannelId(mySubs)
# Получаю список плейлистов с этих каналов
list_anime_text = asyncio.run(get_name_and_id_anime(chanelIds))


def writeYoutubeVideosInDB() -> None:
    # Получаю словарь по каналам, которые я отслеживаю
#    mySubs = getSubs()
    # Получаю уникальные идентификаторы этих каналов
#    chanelIds = getListChannelId(mySubs)
    # Получаю список плейлистов с этих каналов
    # test
    print(list_anime_text)
#    for channelId in chanelIds:
    #        playlists = getChannel(channelId)
#        items = getPlaylistsItems(getUploads(playlists))
#        video_id = getVideoId(items)
#        createCellDB(video_id)


def youtube_parse():
    logging.warning("It is time to start the dramatiq task youtube")
    writeYoutubeVideosInDB()
    process_user_stats.send()
#import logging
#
#from django.db import IntegrityError
#from youtube.models import Youtube_model
#
#from .tasks import process_user_stats
#from .youtube_build import youtube
#
#
#def youtube_parse():
#    logging.warning("It is time to start the dramatiq task youtube")
#
#    # Получаю список ID каналов, на которые я подписан, на которых есть непросмотренные видео.
#    request_subscriptions = youtube.subscriptions().list(
#        part="snippet,contentDetails", maxResults=100, mine=True
#    )
#    response_subscriptions = request_subscriptions.execute()
#
#    def foo_0(n):
#        channelId_newItemCount = {}
#        for x in range(n):
#            newItemCount = response_subscriptions["items"][x]["contentDetails"][
#                "newItemCount"
#            ]
#            channelId = response_subscriptions["items"][x]["snippet"]["resourceId"][
#                "channelId"
#            ]
#            if newItemCount != 0:
#                channelId_newItemCount[channelId] = newItemCount
#        return channelId_newItemCount
#
#    totalResults = response_subscriptions["pageInfo"]["totalResults"]
#    lists_dicts_id_chs = dict(foo_0(totalResults))
#    # Создаю список playlistsId используя список ID каналов по uploads метод channels.
#    for playlistsId, newItemCount in lists_dicts_id_chs.items():
#        request_channels = youtube.channels().list(
#            part="contentDetails", id=playlistsId
#        )
#        playlists = request_channels.execute()
#        uploads = playlists["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
#        # Перебираю полученный список чтобы достать playlistsId
#        # Достаю из каждого плейлиста видео используя playlistsId
#        playlistItems = youtube.playlistItems().list(
#            part="contentDetails", playlistId=uploads, maxResults=10000
#        )
#        response_1 = playlistItems.execute()
#        # Вывожу большой JSON файл в котором есть вся инфа по каждому видео с каналов которые я смотрю.
#        videoId_videoPublishedAt = []
#        for aja, asd in response_1.items():
#            if aja == "items":
#                for ab in asd:
#                    for key_2, value_2 in ab.items():
#                        if key_2 == "contentDetails" and len(value_2) == 2:
#                            videoId_videoPublishedAt.append(value_2)
#        try:
#            sorted_list = sorted(
#                videoId_videoPublishedAt,
#                key=lambda d: d["videoPublishedAt"],
#                reverse=True,
#            )
#        except KeyError:
#            print("That key does not exist!")
#        else:
#            last_video = sorted_list[newItemCount - 1]
#            new_video, created = Youtube_model.objects.update_or_create(
#                    id_video=last_video['videoId']
#                    )
##        try:
##            new_video = Youtube_model.objects.create(id_video=last_video['videoId'])
##        except IntegrityError:
##            pass
##        else:
##            new_video.save(force_update=True)
#    process_user_stats.send()
