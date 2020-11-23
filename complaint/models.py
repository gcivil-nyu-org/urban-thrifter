from django.db import models
from django.contrib.auth.models import User
from donation.models import ResourcePost



STATUS_CHOICES = (
    ("VALID", "Valid"),
    ("PENDING", "Pending"),
    ("INVALID", "Invlaid"),
)


class Complaint(models.Model):
    subject = models.CharField(max_length=100)
    message = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="Pending")
    issuer = models.ForeignKey(User, on_delete=models.CASCADE)
    resource_post = models.ForeignKey(ResourcePost, on_delete=models.CASCADE)
