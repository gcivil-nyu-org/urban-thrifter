from donation.models import ResourcePost
from .models import ReservationPost, Notification
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.template import loader
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator

# from donor_notifications.models import Notification
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, "reservation/reservation_home.html")


def donation_post_list(request):
    # Getting posts based on filters or getting all posts
    url_parameter = request.GET.get("q")
    if url_parameter:
        post_list = ResourcePost.objects.filter(
            title__icontains=url_parameter
        ).order_by("-date_created")
    else:
        post_list = ResourcePost.objects.all().order_by("-date_created")

    # Paginator
    page = request.GET.get("page", 1)
    paginator = Paginator(post_list, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # Ajax code
    if request.is_ajax():
        html = render_to_string(
            template_name="reservation/donation_list.html", context={"posts": posts}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    return render(
        request, "reservation/reservation_home.html", {"posts": posts, "first": "True"}
    )


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
    receiver = request.user
    notifications = Notification.objects.filter(receiver=receiver).order_by("-date")
    template = loader.get_template("donation/notifications.html")

    context = {
        "notifications": notifications,
    }

    return HttpResponse(template.render(context, request))

def helpseeker_notifications(request):
    notifications = Notification.objects.filter(receiver=request.user).order_by("-date")
    template = loader.get_template("reservation/messages.html")

    context = {
        "notifications": notifications,
    }

    return HttpResponse(template.render(context, request))

def read_message(request, id):
    if request.method == "POST":
        notification = Notification.objects.get(id=id)
        notification.is_seen = True
        notification.save()
    return redirect("reservation:reservation-messages")

@method_decorator(login_required, name="dispatch")
class NotificationCheck(View):
    def get(self, request):
        return HttpResponse(
            Notification.objects.filter(is_seen=False, receiver=request.user).count()
        )
        