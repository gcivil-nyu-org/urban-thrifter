from django.db import models


class Complaint(models.Model):
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
