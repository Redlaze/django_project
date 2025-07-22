from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import (
    HttpResponse,
    HttpResponseNotFound,
)
from django.shortcuts import (
    render, redirect,
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
    RegisterUserForm,
    LoginUserForm,
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
        return self.get_posts()


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
        return self.get_posts().filter(
            cat__slug=self.kwargs['cat_slug'],
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        first_post = context['posts'][0]
        title = 'Категория - {}'.format(
            str(first_post.cat),
        )
        cat_selected = first_post.cat_id
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


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'app/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Регистрация',
        )

        context.update(
            **c_def,
        )

        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return redirect('home')



class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'app/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Авторизация',
        )

        context.update(
            **c_def,
        )

        return context

    def get_success_url(self):
        return reverse_lazy('home')


def about(request):
    return render(request, 'app/about.html', {'menu': menu, 'title': 'О сайте'})


def contact(request):
    return HttpResponse("Обратная связь")


# def login(request):
#     return HttpResponse("Авторизация")


def logout_user(request):
    logout(request)

    return redirect('login')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
