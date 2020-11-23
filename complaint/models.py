from django.db import models



STATUS_CHOICES = (
    ("AVAILABLE", "Available"),
    ("RESERVED", "Reserved"),
    ("PENDING", "Pending"),
    ("CLOSED", "Closed"),
)
class Complaint(models.Model):
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default="Available"
    )