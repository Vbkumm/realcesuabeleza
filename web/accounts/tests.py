from django.test import TestCase
from .models import CustomUserManager
from django.test import Client

# Create your tests here.


class CustomUserTestCase(TestCase):
    def setUp(self):
        self.user = CustomUserManager.objects.create(email='test@email.com', password='')
        self.user.set_password('secret')
        self.user.save()
        self.client = Client()
        self.client.login(email='test@email.com', password='secret')
