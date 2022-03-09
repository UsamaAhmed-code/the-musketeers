from django.db import models
import email

# Create your models here.
class CountPage(models.Model):
    no_of_visits = models.IntegerField()


# Create your models here.
class Visits(models.Model):
    no_of_visits=models.IntegerField(max_length=300)



class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.IntegerField()
