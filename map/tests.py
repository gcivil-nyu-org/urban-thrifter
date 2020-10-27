from django.test import TestCase
from django.urls import reverse
from map.apps import MapConfig
from django.test import Client


class MapConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(MapConfig.name, "map")

class GetTest(TestCase):

    @classmethod
    def setUpClass(self):
        # creating instance of a client.
        self.client = Client()

    def test_getLogin(self):
        # Issue a GET request.
        response = self.client.get('/map/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

