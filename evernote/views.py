


import email
from msilib.schema import SelfReg
from re import U
from typing_extensions import Self
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.contrib.auth.models import User, auth
from evernote.models import   Document, Contact
from django.contrib import messages
from .forms import CreateNoteForm
from django.contrib.auth import logout




def registerpage(request):

 
   if request.method == 'POST':
       username = request.POST.get('username')
       email = request.POST.get('email')
       psw1= request.POST.get('psw')
       psw2= request.POST.get('psw-repeat')
     
       if psw1==psw2:
           if User.objects.filter(email=email).exists():
               messages.info(request, 'email already Taken')
               return render(request, 'register.html')
           
           else:     
             user = User.objects.create_user(username=username, email=email, password=psw1)
             user.save();
             messages.info(request, 'sign up successfully')
             return render(request, 'register.html')
           

             
       else :
             messages.info(request, 'password not match')
             return render(request, 'register.html')
   else:   
    return render(request, 'register.html')


def loginpage(request):

     if request.method == 'POST' :

         username = request.POST.get('username')

         password = request.POST['password']
         
         user = auth.authenticate(username=username, password=password)

         if user is not None:
             auth.login(request, user)

             return redirect( '/editor')

         else :
             messages.info(request, 'invalid credentials') 
             return redirect( 'login')

     else :  
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/login')

@login_required
def editor(request):
    id = request.user.id
    id = User.objects.get(id = id)
    docid =int(request.GET.get('docid',0 ))
    documents = Document.objects.filter(author_id=id)
    form = CreateNoteForm()
    username = request.user.username
    user = User.objects.get(username = username)
    author = user

    if request.method == 'POST':
     
      

        docid = int(request.POST.get('docid', 0))
        title = request.POST.get('title')
        content = request.POST.get('content', '')

        if docid > 0:
            document = Document.objects.get(pk=docid)
            document.title = title
            document.content = content
            document.save()

            
    

            return redirect('/editor/?docid='+str(docid) )
        else:
            document = Document.objects.create(title=title, content=content, author=author)
           
            return redirect('/editor' )


    if docid > 0:
        document = Document.objects.get(pk=docid)
    else:
        document = ''

    context={
        
        'docid': docid,
        'documents' : documents,
        'document' : document,

        'author' : author,
        'form' : form, 
       
       
         }


    return render(request, 'editor.html', context)

    

def delete_document(request, docid):
    document = Document.objects.get(pk=docid)
    document.delete()

    return redirect('/editor')


    

   
def contactpage(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        message =request.POST['content']
        contact=Contact(name=name, email=email,content=message)
        contact.save()
    return render(request, "contact.html")    


def edit_username(request):
    if request.method == 'POST':
        username = request.user.username
        newusername = request.POST['newusername']
        newusername2 = request.POST['newusername2']
        password = request.POST['newusername2']
        if newusername != newusername2:
            print("check1")
            messages.info(request, 'Name doesnot match please check')

            return render(request, 'edit_username.html')
        elif User.objects.filter(username=newusername).exists():
            messages.info(request, 'The username is not available')
            return render(request, 'edit_username.html')
        

        else:
            user = User.objects.get(username= username)
            user.username = newusername
            print("okay")
            user.save()

            return redirect('/editor')

    return render(request, 'edit_username.html')

from django.shortcuts import render
from django.db.models import Q


def searchposts(request):
    if request.method == 'GET':
        query= request.GET.get('q')

        submitbutton= request.GET.get('submit')

        if query is not None:
            lookups= Q(title__icontains=query) | Q(content__icontains=query)

            results= Document.objects.filter(lookups).distinct()

            context={'results': results,
                     'submitbutton': submitbutton}

            return render(request, 'editor.html', context)

        else:
            return render(request, 'editor.html')

    else:
        return render(request, 'editor.html')

