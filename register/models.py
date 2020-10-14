from django.db import models
from django.contrib.auth.models import User

class HelpseekerProfile(models.Model):
    BOROUGH_CHOICES=[
        ('MAN', 'Manhattan'),
        ('BRK', 'Brooklyn'),
        ('QUN', 'Queens'),
        ('BRX', 'The Bronx'),
        ('STN', 'Staten Island'),
    ]
    RESOURCE_CATEGORY_CHOICES=[
        ('FOOD', 'Food'),
        ('MDCL', 'Medical/ PPE'),
        ('CLTH', 'Clothing/ Covers'),
        ('ELEC', 'Electronics'),
        ('OTHR', 'Others'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    borough = models.CharField(max_length=3, choices=BOROUGH_CHOICES, blank=False)
    complaint_count = models.IntegerField(default=0, blank=False)
    rc_1 = models.CharField(max_length=4, choices=RESOURCE_CATEGORY_CHOICES, default=None, blank=True, null=True)
    rc_2 = models.CharField(max_length=4, choices=RESOURCE_CATEGORY_CHOICES, default=None, blank=True, null=True)
    rc_3 = models.CharField(max_length=4, choices=RESOURCE_CATEGORY_CHOICES, default=None, blank=True, null=True)