# Create your tests here.
from django.test import TestCase
from .models import ReservationPost
from donation.models import ResourcePost
from register.models import DonorProfile, HelpseekerProfile
from reservation.models import Notification
from django.contrib.auth.models import User

# from django.urls import reverse
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

    def test_reservation_selected_slot_1(self):
        donor = createdonor()
        helpseeker = creathelpseeker()
        donation_post = createdonation(donor)
        reservation = ReservationPost(
            post=donation_post,
            donor=donor,
            helpseeker=helpseeker,
        )
        selected_time = donation_post.dropoff_time_1
        reservation.dropoff_time_request = selected_time
        self.assertEqual(reservation.post.status, "AVAILABLE")
        self.assertEqual(reservation.dropoff_time_request, donation_post.dropoff_time_1)

    def test_reservation_selected_slot_2(self):
        donor = createdonor()
        helpseeker = creathelpseeker()
        donation_post = createdonation(donor)
        reservation = ReservationPost(
            post=donation_post,
            donor=donor,
            helpseeker=helpseeker,
        )
        selected_time = donation_post.dropoff_time_2
        reservation.dropoff_time_request = selected_time
        self.assertEqual(reservation.post.status, "AVAILABLE")
        self.assertEqual(reservation.dropoff_time_request, donation_post.dropoff_time_2)

    def test_reservation_selected_slot_3(self):
        donor = createdonor()
        helpseeker = creathelpseeker()
        donation_post = createdonation(donor)
        reservation = ReservationPost(
            post=donation_post,
            donor=donor,
            helpseeker=helpseeker,
        )
        selected_time = donation_post.dropoff_time_3
        reservation.dropoff_time_request = selected_time
        self.assertEqual(reservation.post.status, "AVAILABLE")
        self.assertEqual(reservation.dropoff_time_request, donation_post.dropoff_time_3)

    def test_reservation_give_notifications(self):
        donor = createdonor()
        helpseeker = creathelpseeker()
        donation_post = createdonation(donor)
        reservation = ReservationPost(
            dropoff_time_request=donation_post.dropoff_time_1,
            post=donation_post,
            donor=donor,
            helpseeker=helpseeker,
        )
        reservation.save()
        self.assertIsNone(reservation.give_notifications(reservation))

    def test_reservation_str(self):
        donor = createdonor()
        helpseeker = creathelpseeker()
        donation_post = createdonation(donor)
        reservation = ReservationPost(
            dropoff_time_request=donation_post.dropoff_time_1,
            post=donation_post,
            donor=donor,
            helpseeker=helpseeker,
        )
        reservation.save()
        self.assertEquals(str(reservation.post.title) + " for " + str(reservation.helpseeker.username),reservation.__str__())


class NotificationTests(TestCase):
    def test_notification_model_isseen(self):
        donor = createdonor()
        helpseeker = creathelpseeker()
        donation_post = createdonation(donor)
        reservation = ReservationPost(
            dropoff_time_request=1,
            post=donation_post,
            donor=donor,
            helpseeker=helpseeker,
        )
        notification = Notification(
            post=reservation,
            sender=helpseeker,
            receiver=donor,
            date=timezone.now(),
        )
        self.assertEqual(notification.is_seen, False)

    def test_notification_model_status(self):
        donor = createdonor()
        helpseeker = creathelpseeker()
        donation_post = createdonation(donor)
        reservation = ReservationPost(
            dropoff_time_request=1,
            post=donation_post,
            donor=donor,
            helpseeker=helpseeker,
        )
        notification = Notification(
            post=reservation,
            sender=helpseeker,
            receiver=donor,
            date=timezone.now(),
        )
        self.assertEqual(notification.notificationstatus, 3)

    def test_notification_model_save(self):
        donor = createdonor()
        helpseeker = creathelpseeker()
        donation_post = createdonation(donor)
        reservation = ReservationPost(
            dropoff_time_request=donation_post.dropoff_time_1,
            post=donation_post,
            donor=donor,
            helpseeker=helpseeker,
        )
        reservation.save()
        notification = Notification(
            post=reservation,
            sender=helpseeker,
            receiver=donor,
            date=timezone.now(),
        )
        self.assertIsNone(notification.save())


class ReservationPostListDeleteTests(TestCase):
    def test_delete_reservation_with_delete_helpseeker(self):
        donor = createdonor()
        helpseeker = creathelpseeker()
        donation_post = createdonation(donor)
        ReservationPost(
            dropoff_time_request=1,
            post=donation_post,
            donor=donor,
            helpseeker=helpseeker,
        )
        user = User.objects.get(username=helpseeker.username)
        user.delete()
        rp = ReservationPost.objects.filter(helpseeker=user)
        self.assertEqual(len(rp), 0)

    def test_delete_notification_with_delete_helpseeker(self):
        donor = createdonor()
        helpseeker = creathelpseeker()
        donation_post = createdonation(donor)
        ReservationPost(
            dropoff_time_request=1,
            post=donation_post,
            donor=donor,
            helpseeker=helpseeker,
        )
        user = User.objects.get(username=helpseeker.username)
        user.delete()
        noti = Notification.objects.filter(sender=helpseeker)
        self.assertEqual(len(noti), 0)
