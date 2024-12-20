from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect

from .models import *

menu = [
    {
        'title': 'О сайте',
        'url_name': 'about',
    },
    {
        'title': 'Добавить статью',
        'url_name': 'add_page',
    },
    {
        'title': 'Обратная связь',
        'url_name': 'contact',
    },
    {
        'title': 'Войти',
        'url_name': 'login',
    },
]


def index(request):
    context = {
        'menu': menu,
        'title': 'Главная страница',
        'cat_selected': 0,
    }

    return render(request, 'app/index.html', context=context)


def about(request):
    return render(request, 'app/about.html', {'menu': menu, 'title': 'О сайте'})


def addpage(request):
    return HttpResponse("Добавление статьи")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def show_post(request, post_id):
    return HttpResponse(f"Отображение статьи с id = {post_id}")

def show_category(request, cat_id):
    context = {
        'menu': menu,
        'title': 'Главная страница',
        'cat_selected': cat_id,
    }

    return render(request, 'app/index.html', context=context)

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')