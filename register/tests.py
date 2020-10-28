from django.test import TestCase
from .models import HelpseekerProfile

class HelpseekerProfileModelTests(TestCase):
    def test_check_for_null_borough(self):
        boro=None
        profileWithNoBorough=HelpseekerProfile(borough=boro)
        self.assertIs(profileWithNoBorough.has_borough(),False)
