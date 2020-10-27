from django.test import TestCase
from django.urls import reverse

class MapConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(SigninConfig.name, "map")

class BaseTest(TestCase):
    
    def setUp(self):
        self.map_url = reverse("map:main-map")

class RunningTest(BaseTest):

    def test_can_view_map_page(self):
        response = self.client.get(self.map_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "map/main.html")
