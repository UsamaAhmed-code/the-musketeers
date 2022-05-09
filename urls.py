from multiprocessing.spawn import import_main_path
from django.urls import URLPattern, path
from evernote import views

urlpatterns = [
   path('', views.loginpage, name= "login"),
    path('register/', views.registerpage, name= "register"),
    path('home/', views.home, name= "home"),
    path('editor/', views.editor, name= "editor"),
     path('delete_document/<int:docid>/', views.delete_document , name='delete_document'),
   path('edit_username/', views.edit_username , name='edit_username'),
      path('edit_password/', views.edit_password, name= "edit_password"),
     path('editor/', views.showusername, name= "editor"),
      
]

