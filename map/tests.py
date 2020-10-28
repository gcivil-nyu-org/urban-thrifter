from django.test import TestCase
from django.urls import reverse
from map.apps import MapConfig


class MapConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(MapConfig.name, "map")


class MapViewTests(TestCase):
    def test_map_view_works(self):
        response = self.client.get(reverse("main-map"))
        self.assertEqual(response.status_code, 200)
