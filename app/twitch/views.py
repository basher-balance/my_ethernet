import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Twitch_model


def streamers_view(request):
    return render(request, "twitch.html")


def streamers_api(request):
    if request.method == 'GET':
        streamers = list(Twitch_model.objects.all().values("streamer", "id"))
        return JsonResponse({"ok": True, "streamers": streamers})

    if request.method == 'DELETE':
        body = json.loads(request.body)
        channel_id = body["id"]
        s = Twitch_model.objects.get(pk=channel_id)
        s.delete()
        return JsonResponse({"ok": True})
