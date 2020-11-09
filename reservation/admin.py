from django.contrib import admin
from .models import ReservationPost, Notification


# Register your models here.
admin.site.register(ReservationPost)
admin.site.register(Notification)