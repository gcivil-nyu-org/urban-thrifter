from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from reservation.models import ReservationPost
import datetime
import pytz
import os
from django.core.mail import send_mail


class Command(BaseCommand):
    help = (
        "Send reminder emails to donors before 15 minutes of the actual donation time"
    )

    def handle(self, *args, **options):
        try:
            acceptedposts = ReservationPost.objects.filter(
                reservationstatus=1,
                dropoff_time_request__gt=datetime.datetime.now(),
                dropoff_time_request__lte=datetime.datetime.now()
                + datetime.timedelta(hours=24),
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
                    + str(acceptedpost.pk)
                )
                message = (
                    "<h1>DONATION DROPOFF REMINDER</h1><p><h3>Just a quick reminder. The dropoff time for donation of <strong>"
                    + str(acceptedpost.post.title)
                    + "</strong> to <strong>"
                    + str(acceptedpost.helpseeker)
                    + "</strong> is at <strong>"
                    + dropoff_time
                    + "</strong>. Here is the link to your post: "
                    + LINK
                    + "</h3></p>"
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
