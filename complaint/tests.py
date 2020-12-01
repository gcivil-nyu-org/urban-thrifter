from django.test import TestCase
from django.urls import reverse
from complaint.apps import ComplaintConfig
from complaint.models import Complaint
from django.utils import timezone
from .models import User
from register.models import DonorProfile, HelpseekerProfile
from donation.models import ResourcePost
from reservation.models import ReservationPost


class ComplaintConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(ComplaintConfig.name, "complaint")


def createdonor():
    donor = User(
        username="donor_unit_test",
        is_active=True,
        email="unittest@unittest.com",
    )
    donor.set_password("Unittestpassword123!")

    donor_prof = DonorProfile(user=donor, complaint_count=0, donation_count=0)
    donor.save()
    donor_prof.save()
    return donor


def createhelpseeker():
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


def create_reservation_post():
    donor = createdonor()
    helpseeker = createhelpseeker()
    donation_post = createdonation(donor)
    reservation = ReservationPost(
        dropoff_time_request=timezone.now(),
        post=donation_post,
        donor=donor,
        helpseeker=helpseeker,
    )
    reservation.save()
    return reservation


class ComplaintViewTests(TestCase):


    def test_map_view_works(self):
        donor = createdonor()
        create_resource_post = createdonation(donor)
        url = reverse("issue-complaint", kwargs={'pk': create_resource_post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_right_complaint_post_request(self):
        reservation_post = create_reservation_post()
        issuer = reservation_post.helpseeker
        receiver = reservation_post.donor
        holder = self.client.post(
            reverse("issue-complaint", kwargs={'pk': reservation_post.post.id}),
            data={
                "subject": "Subject1",
                "message": "I have a problem",
                "image": "",
                "issuer": issuer,
                "receiver": receiver,
                "reservation_post": reservation_post
            },
        )
        self.assertEqual(holder.status_code, 200)


class ComplaintModelTests(TestCase):
    def test_complaint_contains_correct_info(self):
        reservation_post = create_reservation_post()
        issuer = reservation_post.helpseeker
        receiver = reservation_post.donor
        test_complaint_1 = Complaint(
            subject="I hate math",
            message="I hate math",
            uploaded_at=timezone.now(),
            image=None,
            issuer=issuer,
            receiver=receiver,
            reservation_post=reservation_post
        )
        test_complaint_1.save()

        self.assertEquals(
            str(test_complaint_1.issuer.username) + " to " + str(test_complaint_1.receiver.username) + " about " + str(test_complaint_1.reservation_post.__str__()),
            test_complaint_1.__str__()
        )


    def test_complaint_contains_no_data(self):
        form = Complaint()
        form.reservation_post = create_reservation_post()
        form.issuer = form.reservation_post.helpseeker
        form.receiver = form.reservation_post.donor
        self.assertFalse(form.save())

    def test_complaint_contains_wrong_message_data(self):
        form = Complaint(
            subject="hi all,",
            message="",
            uploaded_at=timezone.now(),
            image=None,
        )
        form.reservation_post = create_reservation_post()
        form.issuer = form.reservation_post.helpseeker
        form.receiver = form.reservation_post.donor
        self.assertFalse(form.save())

    def test_complaint_contains_wrong_subject_data(self):
        form = Complaint(
            subject="",
            message="yippie",
            uploaded_at=timezone.now(),
            image=None,
        )
        form.reservation_post = create_reservation_post()
        form.issuer = form.reservation_post.helpseeker
        form.receiver = form.reservation_post.donor
        self.assertFalse(form.save())

    def test_complaint_contains_without_subject_message_data(self):
        form = Complaint(
            uploaded_at=timezone.now(),
            image=None,
        )
        form.reservation_post = create_reservation_post()
        form.issuer = form.reservation_post.helpseeker
        form.receiver = form.reservation_post.donor
        self.assertFalse(form.save())

    def test_complaint_contains_without_image(self):
        form = Complaint(
            subject="hi all,",
            message="yippie",
            uploaded_at=timezone.now(),
        )
        form.reservation_post = create_reservation_post()
        form.issuer = form.reservation_post.helpseeker
        form.receiver = form.reservation_post.donor
        self.assertFalse(form.save())
