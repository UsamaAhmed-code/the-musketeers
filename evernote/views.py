from contextlib import contextmanager
from email import message
from multiprocessing import context
from timeit import repeat
from django.shortcuts import redirect, render
from django.http import HttpResponse
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from evernote.models import  CountPage
from django.contrib import messages

def registerpage(request):

   if request.method == 'POST':
       username = request.POST['username']
       email = request.POST['email']
       psw1= request.POST['psw']
       psw2= request.POST['psw-repeat']
     
       if psw1==psw2:
           if User.objects.filter(email=email).exists():
               messages.info(request, 'Email already Taken')
               return render(request, 'register.html')
           else:     
             user = User.objects.create_user(username=username, email=email, password=psw1)
             user.save();
             return render(request, 'login.html')
             
       else :
             messages.info(request, 'password not match')
             return render(request, 'register.html')
   else:   
    return render(request, 'register.html')


def loginpage(request):

     if request.method == 'POST' :
         username = request.POST['username']
         password = request.POST['password']
         
         user = auth.authenticate(username=username, password=password)

         if user is not None:
             auth.login(request, user)
             return redirect( 'home')
         else :
             messages.info(request, 'invalid credentials') 
             return redirect( 'login')

     else :  
        return render(request, 'login.html')


def home(request):
  count = CountPage.objects.get(id = 1)
  CountPage.objects.filter(id = 1 ).update(content = count.content + 1) 
  count = CountPage.objects.get(id = 1)
  print(count)

  return render(request, 'home.html', {'items' : count })

def logout(request):
    auth.logout(request)
    return redirect('/')
