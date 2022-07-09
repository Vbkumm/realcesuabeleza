from django.test import SimpleTestCase
from django.urls import reverse
from .views import home_view


class HomepageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse(home_view))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse(home_view))
        self.assertTemplateUsed(response, "home.html")

    def test_template_content(self):
        response = self.client.get(reverse(home_view))
        self.assertContains(response, "<h1>Venha fazer parte dessa comunidade que vem revolucionado o mundo da beleza!</h1>")
        self.assertNotContains(response, "Not on the page")

