from django.http import HttpResponse, HttpResponseNotFound
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
    posts = Person.objects.all()
    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Главная страница',
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

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')