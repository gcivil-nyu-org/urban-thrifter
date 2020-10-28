from django.test import TestCase
from .forms import HelpseekerForm

class HelpseekerRegistrationTests(TestCase):
    def test_first_name_label(self):
        form = HelpseekerForm()
        self.assertTrue(form.fields["username"].label == "Username")

    def test_password_label(self):
        form = HelpseekerForm()
        self.assertTrue(form.fields["password1"].label == "Password")

    def test_password2_label(self):
        form = HelpseekerForm()
        self.assertTrue(form.fields["password2"].label == "Confirm Password")

    def test_borough_label(self):
        form = HelpseekerForm()
        self.assertTrue(form.fields["borough"].label == "Borough")

    def test_resource_label(self):
        form = HelpseekerForm()
        self.assertTrue(
            form.fields["resource"].label == "Resources (Optional, select up to 3)"
        )
