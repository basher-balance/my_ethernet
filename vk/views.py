from django.shortcuts import render, redirect
from .models import Vk


def vk(request):
    list_post_vk = list(Vk.objects.filter(_is_expired=False).values('data_post', 'text_post', 'link_post', 'link_image_post', 'id'))
    return render(request, 'vk/vk.html', {'list_post_vk': list_post_vk})


def hidden_post(request, pk):
    '''Функция которая будет скрывать по id пост Хабра'''
    # здесь возможно другой метод у класса Vk
    Vk.hidden(pk)
    return redirect('vk:vk')


def delete_post(request):
    '''Функция удаляющая все новости из базы данных, после удаления и послудующем
    парсинге постов все новости снова будут видны'''
    Vk.objects.all().delete()
    return redirect('vk:vk')
