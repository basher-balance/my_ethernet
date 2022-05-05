import logging
import os

from django.db import IntegrityError
from youtube.models import Youtube_model

from .tasks import process_user_stats
from .youtube_build import youtube


def youtube_parse():
    logging.warning("It is time to start the dramatiq task youtube")

    # Получаю список ID каналов, на которые я подписан, на которых есть непросмотренные видео.
    request_subscriptions = youtube.subscriptions().list(
        part="snippet,contentDetails", maxResults=100, mine=True
    )
    response_subscriptions = request_subscriptions.execute()

    def foo_0(n):
        channelId_newItemCount = {}
        for x in range(n):
            newItemCount = response_subscriptions["items"][x]["contentDetails"][
                "newItemCount"
            ]
            channelId = response_subscriptions["items"][x]["snippet"]["resourceId"][
                "channelId"
            ]
            if newItemCount != 0:
                channelId_newItemCount[channelId] = newItemCount
        return channelId_newItemCount

    totalResults = response_subscriptions["pageInfo"]["totalResults"]
    lists_dicts_id_chs = dict(foo_0(totalResults))
    finally_iframe_youtube = []
    # Создаю список playlistsId используя список ID каналов по uploads метод channels.
    for playlistsId, newItemCount in lists_dicts_id_chs.items():
        request_channels = youtube.channels().list(
            part="contentDetails", id=playlistsId
        )
        playlists = request_channels.execute()
        uploads = playlists["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        #        print(lists_playlists)
        # Перебираю полученный список чтобы достать playlistsId
        # Достаю из каждого плейлиста видео используя playlistsId
        playlistItems = youtube.playlistItems().list(
            part="contentDetails", playlistId=uploads, maxResults=10000
        )
        response_1 = playlistItems.execute()
        # print(response_1)
        # Вывожу большой JSON файл в котором есть вся инфа по каждому видео с каналов которые я смотрю.
        videoId_videoPublishedAt = []
        for aja, asd in response_1.items():
            if aja == "items":
                for ab in asd:
                    for key_2, value_2 in ab.items():
                        if key_2 == "contentDetails" and len(value_2) == 2:
                            videoId_videoPublishedAt.append(value_2)
        try:
            sorted_list = sorted(
                videoId_videoPublishedAt,
                key=lambda d: d["videoPublishedAt"],
                reverse=True,
            )
        except KeyError:
            print("That key does not exist!")
        else:
            # print(sorted_list)
            last_video = sorted_list[newItemCount - 1]
            id_last = last_video["videoId"]
            embeded = youtube.videos().list(part="player", id=id_last)
            id_lastvideoe_embeded = embeded.execute()
            wtf = id_lastvideoe_embeded["items"][0]["player"]["embedHtml"]
        # finally_iframe_youtube.append(wtf)
        try:
            new_video = Youtube_model.objects.create(iframe=wtf)
        except IntegrityError:
            pass
        else:
            new_video.save(force_update=True)
    process_user_stats.send()
