from inspect import BlockFinder
from urllib.parse import urlparse
from django.urls import URLPattern, path
from . import views

#the url patterns store all the urls that are being used. here its the main.
urlpatterns = [
    path('', views.home, name="home"),
    path('/create', views.create, name="create1")
    
]
