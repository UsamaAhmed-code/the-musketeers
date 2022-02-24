from django.shortcuts import render

from django.http import HttpResponse

from evernote.models import  CountPage
def home(request):

 count_num = CountPage.objects.get(id = 1)
 CountPage.objects.filter(id = 1 ).update(content = count_num.content + 1) 
 count_num = CountPage.objects.get(id = 1)
 #print(count_num)

 return render(request,'home.html', {'items' : count_num})


