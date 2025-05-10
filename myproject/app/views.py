from django.contrib.auth.decorators import login_required
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
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import (
    AddPostForm,
)
from .models import *
from .utils import *




class PersonHome(DataMixin, ListView):
    model = Person
    template_name = 'app/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Главная страница',
        )
        context.update(
            **c_def,
        )

        return context

    def get_queryset(self):
        return Person.objects.filter(
            is_published=True,
        )


class ShowPost(DataMixin, DetailView):
    model = Person
    template_name = 'app/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        title = context['post']
        c_def = self.get_user_context(
            title=title,
        )
        context.update(
            **c_def,
        )

        return context


class PersonCategory(DataMixin, ListView):
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

        title = 'Категория - {}'.format(
            str(context['posts'][0].cat),
        )
        cat_selected = context['posts'][0].cat_id
        c_def = self.get_user_context(
            title=title,
            cat_selected=cat_selected,
        )
        context.update(
            **c_def,
        )

        return context


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'app/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Добавление статьи',
        )
        context.update(
            **c_def,
        )

        return context


def about(request):
    return render(request, 'app/about.html', {'menu': menu, 'title': 'О сайте'})


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
