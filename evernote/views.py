
from contextlib import contextmanager
from email import message
from multiprocessing import context
from timeit import repeat
from django.shortcuts import redirect, render
from django.http import HttpResponse
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.models import User, auth

from evernote.models import  CountPage, Document
from django.contrib import messages
from django import forms
from .forms import CreateNote

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

             return redirect( 'editor')
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

    return redirect('/login')

def editor(request):
    docid = int(request.GET.get('docid' , 0))
    documents = Document.objects.all()
    form = CreateNoteForm()

    if request.method == 'POST':
        docid = int(request.POST.get('docid', 0))
        title = request.POST.get('title')
        content = request.POST.get('content', '')

        if docid > 0:
            document = Document.objects.get(pk=docid)
            document.title = title
            document.content = content
            document.save()

            return redirect('/editor' )
        else:
            document = Document.objects.create(title=title, content=content)

            return redirect('/?docid=%i' % document.id)

    if docid > 0:
        document = Document.objects.get(pk=docid)
    else:
        document = ''

    context={
        
        'docid': docid,
        'documents' : documents,
        'document' : document,
        'form' : form    }

    return render(request, 'editor.html', context)

    
def delete_document(request, docid):
    document = Document.objects.get(pk=docid)
    document.delete()

    return redirect('/editor')


    
def edit_username(request):
    if request.method == 'POST':
        username = request.user.username
        newusername = request.POST['newusername']
        newusername2 = request.POST['newusername2']
        password = request.POST['newusername2']
        if newusername != newusername2:
            print("check1")
            messages.info(request, 'Name doesnot match please check')
            return render(request, 'editor.html')
        elif User.objects.filter(username=newusername).exists():
            messages.info(request, 'The username is not available')
            return render(request, 'editor.html')
        elif auth.authenticate(username=username, password=password) is None:
            messages.info(request, 'The password doesnot match!')
            return render(request, 'editor.html')
        else:
            user = User.objects.get(username= username)
            user.username = newusername
            print("okay")
            user.save()
            return redirect('editor/')

    return render(request, 'edit_username.html')

