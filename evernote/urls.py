from django.urls import path
from evernote import views

urlpatterns = [
    path("", views.home, name="home"),
]