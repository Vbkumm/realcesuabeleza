from django.test import TestCase
from .models import BusinessModel
from accounts.models import CustomUserManager
from django.utils import timezone
import pytz
from unittest import mock
# Create your tests here.


class BusinessTestCase(TestCase):
    def setUp(self):
        self.user_1 = CustomUserManager.objects.create_user(email='test@email.com', password='secret',)
        self.user_2 = CustomUserManager.objects.create_user(email='test2@email.com', password='secret2',)

        BusinessModel.objects.create(title="Teste Salao",
                                     slug="tester",
                                     email="testando@tester.com",
                                     description="testando a descricao",
                                     birth_date="13/09/1980",
                                     federal_id="000.000.000-00",
                                     owners=["test@email.com"],
                                     users=["test@email.com", "test2@email.com"],
                                     created_by="test@email.com",
                                     created=timezone.now(),
                                     )
        self.assertFalse(BusinessModel.objects.filter(pk=1).exists())




