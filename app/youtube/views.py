from django.shortcuts import render, redirect
from .models import Youtube_model


def get_youtube(request):
    list_video = list(
        Youtube_model.objects.filter(_is_expired=False).values(
            "id_video",
            "id",
        ),
    )

    return render(
        request,
        "youtube.html",
        {"list_video": list_video},
    )


def hidden_video(request, pk):
    Youtube_model.hidden(pk)
    return redirect("youtube:youtube")
