from django import template
from app.models import *
from django.http import Http404


register = template.Library()


@register.inclusion_tag('app/list_categories.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {'cats': cats, "cat_selected": cat_selected}


@register.simple_tag(name='getposts')
def show_posts(sort='title', cat_selected=0):
    if cat_selected:
        posts = Person.objects.filter(
            cat_id=cat_selected,
        ).order_by(sort)
    else:
        posts = Person.objects.all().order_by(sort)

    if not posts:
        raise Http404()

    return posts