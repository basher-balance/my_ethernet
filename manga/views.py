from django.shortcuts import render, redirect
from .models import Manga


def get_manga(request):
    '''Получает из БД название и ссылку на мангу'''
    name_and_link = list(Manga.objects.filter(_is_expired=False).values('name', 'link', 'id'))
    return render(request, 'manga/manga.html', {
        'name_and_link': name_and_link,
        #        'title': name_and_link[0]['name'],
        #        'link': name_and_link[0]['link'],
        #        'id': name_and_link[0]['id'],
        })


def hidden_manga(request, pk):
    '''Функция которая будет скрывать по id manga'''
    # здесь возможно другой метод у класса Vk
    Manga.hidden(pk)
    return redirect('manga:manga')
