from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from evernote.models import  CountPage


def home(request):
# count = CountPage.objects.get(id = 1)
#count.content = count.content + 1
#count.save()
 count = CountPage.objects.get(id = 1)
 CountPage.objects.filter(id = 1 ).update(content = count.content + 1) 
 count = CountPage.objects.get(id = 1)
 print(count)

 return render(request, 'home.html', {'items' : count})


