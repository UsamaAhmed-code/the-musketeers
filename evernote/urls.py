 feature/user
from multiprocessing.spawn import import_main_path
from django.urls import URLPattern, path
from evernote import views

urlpatterns = [
   path('', views.loginpage, name= "login"),
    path('register/', views.registerpage, name= "register"),
    path('home/', views.home, name= "home")
]

