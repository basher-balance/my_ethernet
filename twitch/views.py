from django.shortcuts import render, redirect

from .models import Twitch_model 


def get_streamer(request):
    streamers = list(Twitch_model.objects.all().values('streamer', 'id'))
    return render(request, 'twitch/twitch.html', {'streamers': streamers })

def delete_streamer(request, pk):
    s = Twitch_model.objects.get(pk=pk)
    s.delete()
    return redirect('twitch:twitch')
