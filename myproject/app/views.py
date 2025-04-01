from django.http import (
    HttpResponse,
    HttpResponseNotFound,
)
from django.shortcuts import (
    render,
)
from django.urls import (
    reverse_lazy,
)
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
)

from .forms import (
    AddPostForm,
)
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


class PersonHome(ListView):
    model = Person
    template_name = 'app/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['menu'] = menu
        contex['title'] = 'Главная страница'
        contex['cat_selected'] = 0

        return contex

    def get_queryset(self):
        return Person.objects.filter(
            is_published=True,
        )


class ShowPost(DetailView):
    model = Person
    template_name = 'app/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = context['post']
        context['menu'] = menu

        return context


class PersonCategory(ListView):
    model =Person
    template_name = 'app/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Person.objects.filter(
            cat__slug=self.kwargs['cat_slug'],
            is_published=True,
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Категория - {}'.format(str(context['posts'][0].cat))
        context['menu'] = menu
        context['cat_selected'] = context['posts'][0].cat_id

        return context


class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'app/addpage.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Добавление статьи'
        context['menu'] = menu

        return context


def about(request):
    return render(request, 'app/about.html', {'menu': menu, 'title': 'О сайте'})


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
