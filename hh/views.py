from django.shortcuts import render, redirect
from .models import Hh
import json


def get_fresh_hh(request):
    hh_list = list(
        Hh.objects.filter(_is_expired=False).values(
            "name",
            "salary",
            "url_id",
            "published",
            "requirement",
            "id",
        ),
    )

    def mutate_hh_items(hh_item):
        hh_item["salary"] = json.loads(hh_item["salary"])
        return hh_item

    mapped_hh_list = map(mutate_hh_items, hh_list)
    hh = list(mapped_hh_list)

    return render(
        request,
        "hh/hh.html",
        {"hh_list": hh},
    )


def hidden_hh(request, pk):
    Hh.hidden(pk)
    return redirect("hh:hh")
