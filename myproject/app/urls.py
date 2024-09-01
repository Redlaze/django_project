from django.urls import path, re_path
from myproject import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
]