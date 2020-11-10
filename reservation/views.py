from donation.models import ResourcePost
from .models import ReservationPost, Notification
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib import messages
from django.template import loader
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator

# from donor_notifications.models import Notification
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, "reservation/reservation_home.html")


class PostListView(ListView):
    # Basic list view
    model = ResourcePost
    # Assign tempalte otherwise it would look for post_list.html
    # as default template
    template_name = "reservation/reservation_home.html"

    # Set context_attribute to post object
    context_object_name = "posts"

    # Add ordering attribute to put most recent post to top
    ordering = ["-date_created"]

    # filters = {'status':'AVAILABLE'}

    # Add pagination
    paginate_by = 5


class ReservationPostListView(ListView):
    # Basic list view
    model = ReservationPost
    # Assign tempalte otherwise it would look for post_list.html
    # as default template
    template_name = "reservation/reservation_list.html"

    # Set context_attribute to post object
    context_object_name = "posts"

    # Add ordering attribute to put most recent post to top
    ordering = ["-date_created"]

    # Add pagination
    paginate_by = 5


def confirmation(request):
    return render(request, "reservation/reservation_confirmation.html")


def confirm_notification(request, id):
    if request.method == "POST":
        notification = Notification.objects.get(id=id)
        resource_post = ResourcePost.objects.get(id=notification.post.post.id)
        reserve_post = ReservationPost.objects.get(id=notification.post.id)
        if "accept" in request.POST:
            # do subscribe
            notification.is_seen = True
            notification.notificationstatus = 1
            notification.is_seen = True
            resource_post.status = "RESERVED"
            resource_post.save()
            notification.save()
            return render(request, "donation/notifications_confirm.html")
        elif "deny" in request.POST:
            # do unsubscribe
            resource_post.status = "AVAILABLE"
            resource_post.save()
            reserve_post.delete()
            notification.delete()
            return redirect("donation:donation-home")


def reservation_function(request, id):
    if request.method == "POST":
        selected_timeslot = request.POST.get("dropoff_time")
        resource_post = ResourcePost.objects.get(id=id)
        try:
            holder = ReservationPost.objects.get(post=resource_post)
        except ReservationPost.DoesNotExist:
            holder = None
        if holder is not None:
            messages.error(
                request, "A reservation for this donation has already been made."
            )
            return redirect("reservation:reservation-home")
        else:
            if selected_timeslot == "1":
                selected_time = resource_post.dropoff_time_1
            elif selected_timeslot == "2":
                selected_time = resource_post.dropoff_time_2
            elif selected_timeslot == "3":
                selected_time = resource_post.dropoff_time_3
            donor_id = User.objects.get(id=resource_post.donor_id)
            helpseeker_id = request.user
            reservation = ReservationPost(
                dropoff_time_request=selected_time,
                post=resource_post,
                donor=donor_id,
                helpseeker=helpseeker_id,
            )
        try:
            reservation.save()
            resource_post.status = "PENDING"
            resource_post.save()
        except Exception:
            resource_post.status = "AVAILABLE"
            resource_post.save()
            reservation.delete()
            messages.error(
                request, "Your reservation was unsuccessful. Please try again!"
            )
            return redirect("reservation:reservation-home")
    return redirect("reservation:reservation-confirmation")


class PostDetailView(DetailView):
    # Basic detail view
    model = ResourcePost
    template_name = "reservation/reservation_request.html"


class ReservationDetailView(DetailView):
    # Basic detail view
    model = ReservationPost
    template_name = "reservation/reservation_detail.html"


def show_notifications(request):
    # print(request.user.id)
    receiver = request.user
    notifications = Notification.objects.filter(receiver=receiver).order_by("-date")
    template = loader.get_template("donation/notifications.html")

    context = {
        "notifications": notifications,
    }

    return HttpResponse(template.render(context, request))


@method_decorator(login_required, name="dispatch")
class NotificationCheck(View):
    def get(self, request):
        # print("Notification Count: ", Notification.objects.filter
        # (is_seen=False, receiver=request.user).count())
        return HttpResponse(
            Notification.objects.filter(is_seen=False, receiver=request.user).count()
        )
