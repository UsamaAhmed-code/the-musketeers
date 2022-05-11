from django.test import TestCase

# Create your tests here.
from django import setup
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
setup()
# Create your tests here.

class URLTests(TestCase):
    def test_testhomepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)