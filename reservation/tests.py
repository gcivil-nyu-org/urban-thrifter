# Create your tests here.
from django.test import TestCase
from .models import ReservationPost
from donation.models import ResourcePost
from register.models import DonorProfile, HelpseekerProfile
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


def createdonor():
    donor = User(
        username="donor_unit_test",
        password="Unittestpassword123!",
        is_active=True,
        email="unittest@unittest.com",
    )
    donor_prof = DonorProfile(user=donor, complaint_count=0, donation_count=0)
    donor.save()
    donor_prof.save()
    return donor


def creathelpseeker():
    helpseeker = User(
        username="hs_unit_test",
        password="Unittestpassword123!",
        is_active=True,
        email="hs_unittest@unittest.com",
    )

    helpseeker_prof = HelpseekerProfile(
        user=helpseeker, borough="MANHATTAN", complaint_count=0, rc_1="FOOD"
    )
    helpseeker.save()
    helpseeker_prof.save()
    return helpseeker


def createdonation(donor):
    donation = ResourcePost(
        title="test",
        description="hi",
        quantity=1,
        dropoff_time_1=timezone.now(),
        dropoff_time_2=timezone.now(),
        dropoff_time_3=timezone.now(),
        date_created=timezone.now(),
        resource_category="FOOD",
        donor=donor,
        status="AVAILABLE",
    )
    donation.save()
    return donation


class ReservationPostTests(TestCase):
    def test_reservation_post(self):
        donor = createdonor()
        helpseeker = creathelpseeker()
        donation_post = createdonation(donor)
        reservation = ReservationPost(
            dropoff_time_request=1,
            post=donation_post,
            donor=donor,
            helpseeker=helpseeker,
        )
        self.assertEqual(reservation.post.status, "AVAILABLE")


class ReservationPostListViewTests(TestCase):
    def test_donation_home(self):
        """
        If no post exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("reservation-home"))
        self.assertEqual(response.status_code, 200)
