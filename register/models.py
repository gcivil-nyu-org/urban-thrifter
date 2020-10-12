from django.db import models

# Create your models here.
class Helpseeker(models.Model):
    BOROUGH_CHOICES=[
        ('Manhattan', 'Manhattan'),
        ('Brooklyn', 'Brooklyn'),
        ('Queens', 'Queens'),
        ('The Bronx', 'The Bronx'),
        ('Staten Island', 'Staten Island'),
    ]
    RESOURCE_CHOICES=[
        ('FOOD', 'Food'),
        ('PPE', 'Personal Protective Equipment'),
        ('CLOTH', 'Clothing And Covers'),
    ]
    
    username = models.CharField(max_length=50, unique=True, blank=False)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True, blank=False)
    password = models.CharField(max_length=128, blank=False)
    borough = models.CharField(max_length=13, choices=BOROUGH_CHOICES, blank=False)
    complaint_count = models.IntegerField(default=0, blank=False)
    datetime_added = models.DateTimeField(auto_now_add=True)
    rc_1 = models.CharField(max_length=5, choices=RESOURCE_CHOICES, default=None, blank=True, null=True)
    rc_2 = models.CharField(max_length=5, choices=RESOURCE_CHOICES, default=None, blank=True, null=True)
    rc_3 = models.CharField(max_length=5, choices=RESOURCE_CHOICES, default=None, blank=True, null=True)
    
    

