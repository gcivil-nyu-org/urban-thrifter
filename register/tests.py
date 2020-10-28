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
            form.fields["resource"].label == "Resources (Optional, select up to 3)")

    def test_form_working(self):
        form = HelpseekerForm(
            data={
                "username": "Jonathan",
                "email": "ponathanjun@gmail.com",
                "password1": "peaches12",
                "password2": "peaches12",
                "borough": "MAN",
                "resource": ["FOOD", "MDCL"],
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_username_wrong(self):
        form = HelpseekerForm(
            data={
                "username": "jon",
                "email": "ponathanjun@gmail.com",
                "password1": "peaches12",
                "password2": "peaches12",
                "borough": "MAN",
                "resource": ["FOOD", "MDCL"],
            }
        )
        self.assertFalse(form.is_valid())

    def test_form_email_wrong(self):
        form = HelpseekerForm(
            data={
                "username": "Jonathan",
                "email": "ponathanjun",
                "password1": "peaches12",
                "password2": "peaches12",
                "borough": "MAN",
                "resource": ["FOOD", "MDCL"],
            }
        )
        self.assertFalse(form.is_valid())

    def test_form_password_wrong(self):
        form = HelpseekerForm(
            data={
                "username": "Jonathan",
                "email": "ponathanjun@gmail.com",
                "password1": "dog",
                "password2": "dog",
                "borough": "MAN",
                "resource": ["FOOD", "MDCL"],
            }
        )
        self.assertFalse(form.is_valid())

    def test_form_password_match_wrong(self):
        form = HelpseekerForm(
            data={
                "username": "Jonathan",
                "email": "ponathanjun@gmail.com",
                "password1": "peaches12",
                "password2": "peaches13",
                "borough": "MAN",
                "resource": ["FOOD", "MDCL"],
            }
        )
        self.assertFalse(form.is_valid())

    def test_form_resource_wrong(self):
        form = HelpseekerForm(
            data={
                "username": "Jonathan",
                "email": "ponathanjun@gmail.com",
                "password1": "peaches12",
                "password2": "peaches12",
                "borough": "MAN",
                "resource": ["dogs", "cats"],
            }
        )
        self.assertFalse(form.is_valid())
