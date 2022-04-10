from turtle import position
from urllib import response
from xml.dom.minidom import Document
from django.test import TestCase
from .models import Document, CountPage
from django import setup
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
setup()
# Create your tests here.

class URLTests(TestCase):
    def test_testhomepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class  DocumentTestCase(TestCase):
    def test_should_add_document(self):
     user = Document.objects.create(title='test', content='email@app.com' )
     user.save()

     self.assertTrue(str(user),'test' )
