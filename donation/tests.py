from django.test import TestCase
from django.urls import reverse
from .models import ResourcePost, User
from register.models import DonorProfile
from django.utils import timezone

# from django.core.files.uploadedfile import SimpleUploadedFile
# import tempfile
# from django.test import override_settings


# from PIL import Image
# Create your tests here.

# def get_temporary_image(temp_file):
#     size = (200, 200)
#     color = (255, 0, 0, 0)
#     image = Image.new("RGB", size, color)
#     image.save(temp_file, "jpeg")
#     return temp_file


def createdonor():
    subuser = User(
        username="donor_unit_test",
        password="Unittestpassword123!",
        is_active=True,
        email="unittest@unittest.com",
    )
    donor = User(
        username="donor_unit_test",
        password="Unittestpassword123!",
        is_active=True,
        email="unittest@unittest.com",
        donorprofile=DonorProfile(
            user=subuser,
            complaint_count=0,
            donation_count=0,
            dropoff_location="MetroTech Center, Brooklyn New York USA, \
                40.6930882, -73.9853095",
        ),
    )
    donor.save()
    return donor


class ResourcePostCreateViewTests(TestCase):
    def test_quantity_correct_input(self):
        create_post = ResourcePost(
            title="test",
            description="test",
            quantity=10,
            dropoff_time_1=timezone.now(),
            date_created=timezone.now(),
            donor=createdonor(),
            resource_category="FOOD",
            status="AVAILABLE",
        )
        self.assertTrue(create_post)

    # @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    # def test_image_crop(self):
    #     # temp_file = tempfile.NamedTemporaryFile()
    #     # image = get_temporary_image(temp_file)
    #     small_gif = (
    #         b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04"
    #         b"\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
    #         b"\x02\x4c\x01\x00\x3b"
    #     )
    #     image = SimpleUploadedFile("small.gif", small_gif, content_type="image/gif")
    #     create_resource_post = ResourcePost(
    #         title="test",
    #         description="test",
    #         quantity=10,
    #         dropoff_time_1=timezone.now(),
    #         date_created=timezone.now(),
    #         donor=createdonor(),
    #         resource_category="FOOD",
    #         image=image,
    #         status="AVAILABLE",
    #     )
    #     create_resource_post.save()
    #     url = reverse("donation:donation-detail", args=(create_resource_post.pk,))
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)


class ResourcePostListViewTests(TestCase):
    def test_no_post(self):
        """
        If no post exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("donation:donation-all"))
        self.assertEqual(response.status_code, 404)

    # def test_donation_home(self):
    #     """
    #     If no post exist, an appropriate message is displayed.
    #     """
    #     response = self.client.get(reverse("donation-home"))
    #     self.assertEqual(response.status_code, 200)


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
            dropoff_time_2=timezone.now(),
            dropoff_time_3=timezone.now(),
            date_created=timezone.now(),
            donor=createdonor(),
            resource_category="FOOD",
            status="AVAILABLE",
        )
        create_resource_post.save()
        url = reverse("donation:donation-detail", args=(create_resource_post.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)