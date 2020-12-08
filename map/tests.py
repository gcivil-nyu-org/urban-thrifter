from django.test import TestCase
from django.urls import reverse
from map.apps import MapConfig
from register.models import HelpseekerProfile
from django.contrib.auth.models import User


def creathelpseeker():
    helpseeker = User(
        username="hs_unit_test",
        is_active=True,
        email="hs_unittest@unittest.com",
    )
    helpseeker.set_password("Unittestpassword123!")

    helpseeker_prof = HelpseekerProfile(
        user=helpseeker, borough="MANHATTAN", complaint_count=0, rc_1="FOOD"
    )
    helpseeker.save()
    helpseeker_prof.save()
    return helpseeker


class MapConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(MapConfig.name, "map")


# this fails
class MapViewTests(TestCase):
    def test_map_view_works(self):
        self.user = creathelpseeker()
        response = self.client.get(reverse("main-map"))
        self.assertEqual(response.status_code, 200)
