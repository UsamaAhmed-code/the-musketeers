from inspect import BlockFinder
from urllib.parse import urlparse
from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    
]