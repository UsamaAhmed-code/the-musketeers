from django.db import models

# Create your models here.
class CountPage(models.Model):
    no_of_visits = models.IntegerField()
   
