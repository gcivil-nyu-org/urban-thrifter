from django.db import models
from django.contrib.auth.models import User
from reservation.models import ReservationPost



STATUS_CHOICES = (
    ("PENDING", "Pending"),
    ("VALID", "Valid"),
    ("INVALID", "Invlaid"),
)


class Complaint(models.Model):
    subject = models.CharField(max_length=100)
    message = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="PENDING")
    issuer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="issuer_id")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver_id")
    reservation_post = models.ForeignKey(ReservationPost, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.issuer:
            self.issuer = self.user
        if not self.receiver:
            if self.user.helpseekerprofile:
                self.receiver = self.reservation_post.donor
            elif self.user.donorprofile:
                self.receiver = self.reservation_post.helpseeker
            else: #if admin
                self.receiver = self.issuer

        super().save(*args, **kwargs)
