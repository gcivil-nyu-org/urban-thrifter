from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from donation.models import ResourcePost
from django.urls import reverse
from django.db.models.signals import post_save


# Create your models here.
class ReservationPost(models.Model):
    Reservation_Status = ((1, "accept"), (2, "reject"), (3, "pending"))
    dropoff_time_request = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(ResourcePost, on_delete=models.CASCADE)
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="donor_id")
    helpseeker = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="helpseeker_id"
    )
    date_created = models.DateTimeField(default=timezone.now)
    reservationstatus = models.IntegerField(
        choices=Reservation_Status, default=Reservation_Status[2][0]
    )

    # TODO: generate reservation ID token as primary key?
    # TODO: return reservation ID in __str__
    def __str__(self):
        return str(self.post.title) + " for " + str(self.helpseeker.username)

    def give_notifications(sender, instance, *args, **kwargs):
        reservationpost = instance
        if (
            reservationpost.reservationstatus == 1
            or reservationpost.reservationstatus == 2
        ):
            return
        reservepost = reservationpost.post
        helpseker = reservationpost.helpseeker
        notify = Notification(
            post=reservationpost, sender=helpseker, receiver=reservepost.donor
        )
        notify.save()

    # Reverse would return the full url as a string and
    # let the view redirect for us

    def get_absolute_url(self):
        # return the path of the specific post
        return reverse("reservation:reservation-detail", kwargs={"pk": self.pk})


class Notification(models.Model):
    NOTIFICATION_STATUS = ((1, "ACCEPT"), (2, "REJECT"), (3, "PENDING"))
    post = models.ForeignKey(
        ReservationPost,
        on_delete=models.CASCADE,
        related_name="noti_post",
        blank=True,
        null=True,
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="noti_from_user"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="noti_to_user"
    )
    notificationstatus = models.IntegerField(
        choices=NOTIFICATION_STATUS, default=NOTIFICATION_STATUS[2][0]
    )
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
    __original_notificationstatus = None

    def __init__(self, *args, **kwargs):
        super(Notification, self).__init__(*args, **kwargs)
        self.__original_notificationstatus = self.notificationstatus

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.notificationstatus != self.__original_notificationstatus:
            # status changed
            reservation_post = self.post
            helpseeker = self.sender
            donor = self.receiver
            notification_status = self.notificationstatus
            notify = Notification(
                post=reservation_post,
                sender=donor,
                receiver=helpseeker,
                notificationstatus=notification_status,
            )
            notify.save()
        super(Notification, self).save(force_insert, force_update, *args, **kwargs)
        self.__original_notificationstatus = self.notificationstatus

    def __str__(self):
        return (
            str(self.sender.username)
            + " to "
            + str(self.receiver.username)
            + " for "
            + str(self.post.post.title)
        )


post_save.connect(ReservationPost.give_notifications, sender=ReservationPost)
