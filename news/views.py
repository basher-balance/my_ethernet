from django.shortcuts import render, redirect
from .models import New


def get_fresh_news(request):
    """Передаёт в переменную список нескрытых новостей из БД"""

    list_news = list(
        New.objects.filter(_is_expired=False).values(
            "news",
            "link_news",
            "date_added",
            "id",
        ),
    )

    return render(
        request,
        "news/news.html",
        {"list_news": list_news},
    )


def hidden_news(request, pk):
    New.hidden(pk)
    return redirect("news:news")


def delete_news(request):
    New.objects.all().delete()
    return redirect("news:news")
