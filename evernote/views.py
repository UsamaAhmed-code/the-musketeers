


from email.message import EmailMessage
from multiprocessing import context
from pickle import FALSE
from telnetlib import DO

from typing_extensions import Self
from xml.sax import xmlreader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.contrib.auth.models import User, auth
from SDPproject.settings import EMAIL_HOST_USER
from evernote.models import   Document, Contact
from django.contrib import messages
from .forms import CreateNoteForm, Share_the_PostForm
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

           if User.objects.filter(username=username).exists():
               messages.info(request, 'username already Taken')
               return render(request, 'register.html')
            

           else:     
             user = User.objects.create_user(username=username, email=email, password=psw1)
             user.save();


            
             return redirect( 'login')

            

           

             messages.info(request, 'sign up successfully')
             return render(request, 'register.html')
           


             
       else :
             messages.info(request, 'password not match')
             context={
                      'username' : username,
                      'email' : email,
             }
             return render(request, 'register.html', context)
   else:   
    return render(request, 'register.html')


def loginpage(request):

     if request.method == 'POST' :

         username = request.POST.get('username')

         password = request.POST['password']
         
         user = auth.authenticate(username=username, password=password)

         if user is not None:
             auth.login(request, user)

             return redirect('/editor')

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
            if Document.objects.filter(title=title).exists():
               messages.info(request, 'title already Taken')
               return redirect('/editor/?docid='+str(docid) )
              
            else:
                 document = Document.objects.create(title=title, content=content, author=author )
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



def edit_password(request):
    if request.method == 'POST':
        username = request.user.username
        #userpassword = request.user.password
        user = User.objects.get(username= username)
        oldpassword = request.POST['oldpassword']
        newpassword1 = request.POST['newpassword1']
        newpassword2 = request.POST['newpassword2']
        

        if user.check_password(oldpassword) != True:
            messages.info(request, 'The password is wrong!. Please check again')
            return render(request, 'edit_password.html')
        elif newpassword1 != newpassword2:
            print("check1")
            messages.info(request, 'New passwords donot match please check')
            return render(request, 'edit_password.html')
        elif user.check_password(newpassword1) == True:
            messages.info(request, 'Please use new password for the login.')
            return render(request, 'edit_password.html')
        
        else:

            
            user.set_password(newpassword1)
            print("okay")
            user.save()
            return redirect('/editor/')

    return render(request, 'edit_password.html')
from django.shortcuts import render
from django.db.models import Q


def searchposts(request):


    if request.method == 'POST':
        query= request.POST.get('q')

        submitbutton= request.POST.get('submit')

        if query is None:
          return render(request, 'editor.html')


        if query is not None:
            lookups= Q(title__icontains=query) | Q(content__icontains=query)


            results= Document.objects.filter(lookups)

           

            results= Document.objects.filter(lookups).distinct()


            context={'results': results,
                     'submitbutton': submitbutton}


            return render(request, 'search.html', context)

        else:
            return render(request, 'search.html')


    else:
        return render(request, 'editor.html')


def check_change(request):

    docid = int(request.POST.get('docid', 0))
    title = request.POST.get('title')
    content = request.POST.get('content', '')

    if docid > 0:
        document = Document.objects.get(pk=docid)
        document.title = title
        document.content = content
        document.save()
        return HttpResponse("Auto Saved")
    else:
        document = Document.objects.create(title=title, content=content,)

        return HttpResponse("Not Saved")
           
from django.core.mail import EmailMultiAlternatives
from SDPproject.settings import EMAIL_HOST_USER




def send_mail_plain_with_file(request):
    message = request.POST.get('message', '')
    subject = request.POST.get('subject', '')
    mail_id = request.POST.get('email', '')
    email = EmailMultiAlternatives(subject, message, EMAIL_HOST_USER, [mail_id])
    email.content_subtype = 'html'

    file = request.FILES['file']
    email.attach(file.name, file.read(), file.content_type)

    email.send()
    messages.info(request, 'Email send Successfully')
    return render(request, 'email.html')    

def email(request):
   
    return render(request, 'email.html')    

def favor(request):
    docid = int(request.POST['docid'])
    document = Document.objects.get(pk=docid)
    if document.favorites == True:
        document.favorites = False
    else:
        document.favorites = True
    document.save()
    #return redirect('/editor')
    return render(request, 'editor.html')


