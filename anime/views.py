from django.shortcuts import render, redirect

from .models import Anime


def get_fresh_anime(request):
    list_anime = list(
        Anime.objects.filter(_is_expired=False).values(
            "title_anime", "link_anime", "date_added", "id"
        )
    )
    return render(request, "anime/anime.html", {"list_anime": list_anime})


def hidden_anime(request, pk):
    Anime.hidden(pk)
    return redirect("anime:anime")
