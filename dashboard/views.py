from django.shortcuts import render, redirect
from .models import Dashboard


def get_undetected_anime(request):
    list_undetected_anime = list(
        Dashboard.objects.all().values(
            "title_undetected_anime", "date_added", "id"
        )
    )
    return render(request, "dashboard/dashboard.html", {"list_undetected_anime": list_undetected_anime})


#def delete_anime(request, k):
#    Dashboard.delete_from_anime_parse_list(k)
#    return redirect("dashboard:dashboard")
