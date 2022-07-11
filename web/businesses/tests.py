from django.test import TestCase
from .models import BusinessModel
from accounts.models import CustomUserManager
from django.utils import timezone


class BusinessTestCase(TestCase):
    def setUp(self):
        self.user_1 = CustomUserManager.objects.create_user(email='test@email.com', password='secret',)
        self.user_2 = CustomUserManager.objects.create_user(email='test2@email.com', password='secret2',)

        self.business = BusinessModel.objects.create(title="Teste Salao",
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
        self.assertTrue(isinstance(self.business, BusinessModel))
        self.assertEqual(self.business.slug, "tester",)
        self.assertFalse(BusinessModel.objects.filter(pk=1).exists())
        self.assertEqual(BusinessModel.objects.count(), 1)
        business = BusinessModel.objects.get(pk=1)
        return business
