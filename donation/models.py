from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

# Import reverse
from django.urls import reverse

# from django.contrib.auth.models import User
from places.fields import PlacesField
from django.contrib.auth.models import User

# User Models save database specifically for USERS
RESROUCE_CATEGORY_CHOICES = (
    ("FOOD", "Food"),
    ("MDCL", "Medical/ PPE"),
    ("CLTH", "Clothing/ Covers"),
    ("ELEC", "Electronics"),
    ("OTHR", "Others"),
)
STATUS_CHOICES = (
    ("AVAILABLE", "Available"),
    ("RESERVED", "Reserved"),
    ("PENDING", "Pending"),
    ("CLOSED", "Closed"),
)


class ResourcePost(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    dropoff_time_1 = models.DateTimeField(default=timezone.now)
    dropoff_time_2 = models.DateTimeField(blank=True, null=True)
    dropoff_time_3 = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    dropoff_location = PlacesField()
    resource_category = models.CharField(
        max_length=100, choices=RESROUCE_CATEGORY_CHOICES
    )
    image = models.ImageField(
        default="donation-pics/default.jpg", upload_to="donation-pics", blank=True
    )
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default="Available"
    )

    # Dunder (abbr. for Double Under)/Magic str method
    # define how the object is printed
    def __str__(self):
        return self.title

    # Reverse would return the full url as a string and
    # let the view redirect for us
    def get_absolute_url(self):
        # return the path of the specific post
        return reverse("donation:donation-detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not self.dropoff_location:
            self.dropoff_location = self.donor.donorprofile.dropoff_location
        super().save(*args, **kwargs)
