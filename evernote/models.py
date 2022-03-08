from django.db import models

# Create your models here.
class CountPage(models.Model):
    no_of_visits = models.IntegerField()
   from django.db import models

# Create your models here.
class Visits(models.Model):
    no_of_visits=models.IntegerField(max_length=300)
