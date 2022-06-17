from django.shortcuts import render, redirect
from .models import Serial
from anime.models import ListAnime
from torrents.models import ListSerials


def get_fresh_serials(request):
    serials_list = list(
        Serial.objects.filter(_is_expired=False).values(
            "title",
            "img",
            "data",
            "serial_and_season",
            "episode",
            "id",
        ),
    )
    return render(
        request,
        "serials.html",
        {"serials_list": serials_list},
    )


def hidden_serial(request, pk):
    Serial.hidden(pk)
    return redirect("serials:serials")


def del_serial(request, pk):
    Serial.d_serial(pk)
    return redirect("serials:serials")


def add_anime_parse(request, pk):
    obj = Serial.objects.get(pk=pk).title
    add_obj, created = ListAnime.objects.update_or_create(title=obj)
    return redirect("serials:serials")


def add_torrent(request, pk):
    obj = Serial.objects.get(pk=pk).title
    add_obj, created = ListSerials.objects.update_or_create(title=obj)
    return redirect("serials:serials")
