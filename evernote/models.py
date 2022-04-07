
import email
from lzma import MODE_NORMAL
from xml.dom.minidom import Document
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CountPage(models.Model):
    content = models.IntegerField()

class Document(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Meta:
    ordering = ('title', )    


