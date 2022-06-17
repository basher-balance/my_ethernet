from django.shortcuts import render, redirect
from .models import Torrent


def get_fresh_torrent(request):
    """Передаёт в переменную список нескрытых новостей из БД"""

    torrents_list = list(
        Torrent.objects.filter(_is_expired=False).values(
            "title",
            "link",
            "published",
            "id",
        ),
    )

    return render(
        request,
        "torrents.html",
        {"torrents_list": torrents_list},
    )


def hidden_torrent(request, pk):
    Torrent.hidden(pk)
    return redirect("torrents:torrents")
