from django.test import TestCase
from django.urls import reverse
from complaint.apps import ComplaintConfig
from complaint.models import Complaint
from django.utils import timezone


class ComplaintConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(ComplaintConfig.name, "complaint")


class ComplaintViewTests(TestCase):
    def test_map_view_works(self):
        response = self.client.get(reverse("issue-complaint"))
        self.assertEqual(response.status_code, 200)


class ComplaintModelTests(TestCase):
    def test_complaint_contains_correct_info(self):
        test_complaint_1 = Complaint(
            subject="I hate math",
            message="I hate math",
            uploaded_at=timezone.now(),
            image=None,
        )
        test_complaint_1.save()

        response = self.client.get(reverse("issue-complaint"))
        self.assertEqual(response.status_code, 200)
