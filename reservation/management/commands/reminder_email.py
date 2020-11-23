from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from reservation.models import ReservationPost, Notification
from register.models import DonorProfile

class ReminderEmail(BaseCommand):
    help = 'Send reminder emails to donors before 15 minutes of the actual donation time'

    def handle(self):
        try:
            notifications = Notification.objects.filter(notificationstatus='ACCEPT', post.Exists(DonorProfile.objects.filter(sender__eq=OuterRef('pk'))))
            # User.objects.filter(Exists(Reports.objects.filter(user__eq=OuterRef('pk'))))
            for resourcepost in resourceposts:
                 if 
        except FieldDoesNotExist:
            self.stdout.write(self.style.ERROR('Field "title" does not exist.'))
            return

        self.stdout.write(self.style.SUCCESS('Successfully printed all Book titles'))
        return