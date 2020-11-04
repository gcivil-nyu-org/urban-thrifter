from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from donation.models import ResourcePost

# from places.fields import PlacesField
from django.urls import reverse


# Create your models here.
class ReservationPost(models.Model):

    dropoff_time_request = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(ResourcePost, on_delete=models.CASCADE)
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="donor_id")
    helpseeker = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="helpseeker_id"
    )

    # TODO: generate reservation ID token as primary key?
    # TODO: return reservation ID in __str__
    # def __str__(self):
    # return self.title

    # Reverse would return the full url as a string and
    # let the view redirect for us
    def get_absolute_url(self):
        # return the path of the specific post
        return reverse("reservation-detail", kwargs={"pk": self.pk})
