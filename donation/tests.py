from django.test import TestCase
from django.urls import reverse
from .models import ResourcePost
from django.utils import timezone

# Create your tests here.


class ResourcePostCreateViewTests(TestCase):
    def test_quantity_non_numeric_input(self):
        create_post = ResourcePost(
            title="test",
            description="test",
            quantity="hello",
            dropoff_time_1=timezone.now(),
            date_created=timezone.now(),
            resource_category="FOOD",
        )
        self.assertFalse(create_post.check_quantity())

    def test_quantity_negative_input(self):
        create_post = ResourcePost(
            title="test",
            description="test",
            quantity=-1,
            dropoff_time_1=timezone.now(),
            date_created=timezone.now(),
            resource_category="FOOD",
        )
        self.assertFalse(create_post.check_quantity())

    def test_quantity_correct_input(self):
        create_post = ResourcePost(
            title="test",
            description="test",
            quantity=10,
            dropoff_time_1=timezone.now(),
            date_created=timezone.now(),
            resource_category="FOOD",
        )
        self.assertTrue(create_post.check_quantity())


class ResourcePostListViewTests(TestCase):
    def test_no_post(self):
        """
        If no post exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("donation-all"))
        self.assertEqual(response.status_code, 200)


class HomepageViewTests(TestCase):
    def test_homepage(self):
        """
        If no post exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)


class ResourcePostDetailViewTests(TestCase):
    def test_regular_post(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        create_resource_post = ResourcePost(
            title="test",
            description="test",
            quantity=10,
            dropoff_time_1=timezone.now(),
            date_created=timezone.now(),
            resource_category="FOOD",
        )
        create_resource_post.save()
        url = reverse("donation-detail", args=(create_resource_post.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
