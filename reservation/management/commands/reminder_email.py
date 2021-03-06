from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from reservation.models import ReservationPost
import datetime
import pytz
import os
from django.core.mail import send_mail
from django.utils import timezone


class Command(BaseCommand):
    help = "Send reminder emails to donors when <=10 minutes left for their actual donation time"

    def handle(self, *args, **options):
        try:
            acceptedposts = ReservationPost.objects.filter(
                reservationstatus=1,
                dropoff_time_request__gt=timezone.now(),
                dropoff_time_request__lte=timezone.now()
                + datetime.timedelta(minutes=10),
            )
            email_subject = "Reminder for your incoming donation dropoff"
            for acceptedpost in acceptedposts:
                print(acceptedpost.dropoff_time_request)
                to_email = User.objects.filter(id=acceptedpost.donor.pk).values("email")
                dropoff_time = str(
                    acceptedpost.dropoff_time_request.astimezone(
                        pytz.timezone("US/Eastern")
                    ).strftime("%b %d %Y %-I:%M %p")
                )
                LINK = (
                    "https://"
                    + str(os.environ.get("DOMAIN_NAME"))
                    + "/donation/post/"
                    + str(acceptedpost.post.pk)
                )
                message = (
                    "<h1>DONATION DROP-OFF REMINDER</h1><p><h3>Just a quick reminder. The dropoff time for donation of <strong>"
                    + str(acceptedpost.post.title)
                    + "</strong> to <strong>"
                    + str(acceptedpost.helpseeker)
                    + "</strong> is at <strong>"
                    + dropoff_time
                    + ".</strong></h3></p><p><h3><a href="
                    + LINK
                    + ">Click here to view your upcoming donation drop-off details</a></h3></p>"
                    + "</h3></p><p><h3>NOTE: You must be logged in to view the post.</h3></p><p><h3>Best,</h3></p><p><h3>Team Urban Thrifter</h3></p>"
                )
                send_mail(
                    email_subject,
                    message,
                    "nyu.django.unchained@gmail.com",
                    [to_email[0]["email"]],
                    html_message=message,
                    fail_silently=False,
                )
        except Exception as e:
            print(e)
            return
        return
