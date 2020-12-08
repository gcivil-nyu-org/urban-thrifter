from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from .models import ResourcePost, User
from reservation.models import ReservationPost
from bootstrap_datepicker_plus import DateTimePickerInput
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import os
import datetime
from register.models import HelpseekerProfile
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

# , UserPassesTestMixin


# Create your views here.


def homepage(request):
    # Redirect to login page
    return render(request, "donation/homepage.html")


def login_redirect_view(request):
    # Redirect to login page
    return render(request, "donation/login_redirect.html")


def home(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    if HelpseekerProfile.objects.filter(user=user):
        raise PermissionDenied
    post_list = ResourcePost.objects.filter(donor=user).order_by("-date_created")

    expired_donation_posts = post_list.filter(
        status="EXPIRED",
    ).first()

    reserve_post_list = ReservationPost.objects.filter(donor=user).order_by(
        "-date_created"
    )
    reserved_donation_posts = reserve_post_list.filter(
        reservationstatus=1, post__status__in=["Reserved", "RESERVED"]
    )
    available_donation_posts = post_list.filter(status__in=["Available", "AVAILABLE"])

    close_reservation_15_min(reserved_donation_posts)
    closed_reservation_posts = reserve_post_list.filter(
        reservationstatus=1, post__status__in=["Closed", "CLOSED"]
    )
    # page = request.GET.get("page", 1)
    # paginator = Paginator(post_list, 3)
    # try:
    #     post_list = paginator.page(page)
    # except PageNotAnInteger:
    #     post_list = paginator.page(1)
    # except EmptyPage:
    #     post_list = paginator.page(paginator.num_pages)
    context = {
        "expired_donation_posts": expired_donation_posts,
        "reserved_donation_posts": reserved_donation_posts,
        "available_donation_posts": available_donation_posts,
        "closed_reservation_posts": closed_reservation_posts,
    }

    return render(request, "donation/reservation_status_nav.html", context)


def close_reservation_15_min(reserved_donation_posts):
    try:
        for reserve_post in reserved_donation_posts:
            if (
                reserve_post.post.status != "CLOSED"
                and reserve_post.dropoff_time_request + datetime.timedelta(minutes=15)
                <= timezone.now()
            ):
                reserve_post.post.status = "CLOSED"
                reserve_post.post.save()
        return
    except Exception as e:
        print(e)


# All Donations View
class PostListView(ListView):
    # Basic list view
    model = ResourcePost
    # Assign tempalte otherwise it would look for post_list.html
    # as default template
    template_name = "donation/reservation_status_nav.html"

    # Set context_attribute to post object
    context_object_name = "donation_posts_2"

    # Add ordering attribute to put most recent post to top
    ordering = ["-date_created"]

    # Add pagination
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return ResourcePost.objects.filter(donor=user).order_by("-date_created")


# Post Donation View
class PostCreateView(LoginRequiredMixin, CreateView):
    # Basic create view
    login_url = "/login/"
    redirect_field_name = ""
    model = ResourcePost
    fields = [
        "title",
        "image",
        "description",
        "quantity",
        "dropoff_time_1",
        "dropoff_time_2",
        "dropoff_time_3",
        "resource_category",
        "dropoff_location",
    ]

    def get_form(self):
        if HelpseekerProfile.objects.filter(user=self.request.user):
            raise PermissionDenied
        form = super().get_form()
        form.fields["dropoff_time_1"].widget = DateTimePickerInput()
        form.fields["dropoff_time_2"].widget = DateTimePickerInput()
        form.fields["dropoff_time_3"].widget = DateTimePickerInput()
        form.fields[
            "dropoff_time_1"
        ].label = "<span class='ut-tooltip'>Dropoff Time 1 (EST)<span class='tooltiptext'>Currently our service only supports users in the Greater New York Area</span></span>"
        form.fields["dropoff_time_2"].label = "Dropoff Time 2 (EST)"
        form.fields["dropoff_time_3"].label = "Dropoff Time 3 (EST)"
        return form

    # Overwrite form valid method
    def form_valid(self, form):
        form.instance.donor = self.request.user
        if (
            not form.cleaned_data["dropoff_location"]
            and not form.instance.donor.donorprofile.dropoff_location
        ):
            messages.error(self.request, "Please input your dropoff location.")
            return super().form_invalid(form)

        dropoff_time_1 = form.cleaned_data["dropoff_time_1"]
        dropoff_time_2 = form.cleaned_data["dropoff_time_2"]
        dropoff_time_3 = form.cleaned_data["dropoff_time_3"]
        if (
            dropoff_time_1
            and dropoff_time_1 <= timezone.now()
            or dropoff_time_2
            and dropoff_time_2 <= timezone.now()
            or dropoff_time_3
            and dropoff_time_3 <= timezone.now()
        ):
            messages.error(
                self.request, "Please ensure your dropoff time is in the future."
            )
            return super().form_invalid(form)
        if (
            dropoff_time_1 == dropoff_time_2
            or dropoff_time_2
            and dropoff_time_3
            and dropoff_time_2 == dropoff_time_3
            or dropoff_time_3 == dropoff_time_1
        ):
            messages.error(
                self.request, "Please ensure your dropoff times aren't repetitive."
            )
            return super().form_invalid(form)

        return super().form_valid(form)


# Donation Detail View
class PostDetailView(LoginRequiredMixin, DetailView):
    # Basic detail view
    model = ResourcePost

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context["mapbox_access_token"] = "pk." + os.environ.get("MAPBOX_KEY")
        return context


# Donation Update View
class PostUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    # Basic detail view
    model = ResourcePost
    fields = [
        "title",
        "quantity",
        "description",
        "resource_category",
        "dropoff_time_1",
        "dropoff_time_2",
        "dropoff_time_3",
        "dropoff_location",
    ]
    template_name = "donation/resourcepost_update.html"
    success_message = "Donation post updated successfully."

    # Overwrite form valid method
    def form_valid(self, form):
        form.instance.donor = self.request.user
        if (
            not form.cleaned_data["dropoff_location"]
            and not form.instance.donor.donorprofile.dropoff_location
        ):
            messages.error(self.request, "Please input your dropoff location.")
            return super().form_invalid(form)

        dropoff_time_1 = form.cleaned_data["dropoff_time_1"]
        dropoff_time_2 = form.cleaned_data["dropoff_time_2"]
        dropoff_time_3 = form.cleaned_data["dropoff_time_3"]
        if (
            dropoff_time_1
            and dropoff_time_1 <= timezone.now()
            or dropoff_time_2
            and dropoff_time_2 <= timezone.now()
            or dropoff_time_3
            and dropoff_time_3 <= timezone.now()
        ):
            messages.error(
                self.request, "Please ensure your dropoff time is in the future."
            )
            return super().form_invalid(form)
        if (
            dropoff_time_1 == dropoff_time_2
            or dropoff_time_2
            and dropoff_time_3
            and dropoff_time_2 == dropoff_time_3
            or dropoff_time_3 == dropoff_time_1
        ):
            messages.error(
                self.request, "Please ensure your dropoff times aren't repetitive."
            )
            return super().form_invalid(form)
        form.instance.status = "AVAILABLE"
        return super().form_valid(form)

    def get_form(self):
        form = super().get_form()
        form.fields["dropoff_time_1"].widget = DateTimePickerInput()
        form.fields["dropoff_time_2"].widget = DateTimePickerInput()
        form.fields["dropoff_time_3"].widget = DateTimePickerInput()
        form.fields["dropoff_time_1"].label = "Dropoff Time 1 (EST)"
        form.fields["dropoff_time_2"].label = "Dropoff Time 2 (EST)"
        form.fields["dropoff_time_3"].label = "Dropoff Time 3 (EST)"
        return form


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    # Basic delete view
    model = ResourcePost

    # Redirect to homepage after delete succesfully
    success_url = "/donation"

    # Make sure the post owner can delete the post
    def test_func(self):
        # Retrieve the current post
        post = self.get_object()
        # Check if the current user is the author of the post
        if self.request.user == post.donor:
            return True
        return False


@login_required
def get_resource_post(request):
    user = request.user

    curr_user_rc_1 = user.helpseekerprofile.rc_1
    curr_user_rc_2 = user.helpseekerprofile.rc_2
    curr_user_rc_3 = user.helpseekerprofile.rc_3

    posts = ResourcePost.objects.filter(status__in=["Available", "AVAILABLE"])
    passingList = []
    for post in posts:
        if post.date_created >= user.helpseekerprofile.message_timer_before and (
            post.resource_category == curr_user_rc_1
            or post.resource_category == curr_user_rc_2
            or post.resource_category == curr_user_rc_3
        ):
            # sending id, title, description, because mabye we can use it to make a message popup
            notiPost = {
                "id": post.id,
                "title": post.title,
                "description": post.description,
            }
            passingList.append(notiPost)
    context = {"resource_posts": passingList}

    return JsonResponse(context)


# funciton based view version of messagelistview
def watchlist_view(request):
    user = request.user

    time_now = timezone.now()
    timestamp_interval = [user.helpseekerprofile.message_timer_before, time_now]
    user.helpseekerprofile.message_timer_before = time_now
    # https://stackoverflow.com/questions/53146840/change-model-field-value-after-button-click/53147979
    user.helpseekerprofile.save(update_fields=["message_timer_before"])

    # https://stackoverflow.com/questions/64838254/making-multiple-filters-in-function-filter-django
    post_list = ResourcePost.objects.filter(
        resource_category__in=[
            user.helpseekerprofile.rc_1,
            user.helpseekerprofile.rc_2,
            user.helpseekerprofile.rc_3,
        ],
        status__in=["AVAILABLE", "Available"],
    ).order_by("-date_created")

    new_post_list = post_list.filter(
        date_created__gte=timestamp_interval[0], date_created__lte=timestamp_interval[1]
    )

    page = request.GET.get("page", 1)
    paginator = Paginator(post_list, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        "mapbox_access_token": "pk." + os.environ.get("MAPBOX_KEY"),
        "timestamp_interval": timestamp_interval,
        "posts": posts,
        "new_posts": new_post_list,
    }
    return render(request, "donation/messages_home.html", context)


# # class based view version of messagelistview
# class MessageListView(ListView):
#     # Basic list view
#     model = ResourcePost
#     # Assign tempalte otherwise it would look for post_list.html
#     # as default template
#     template_name = "donation/messages_home.html"

#     # Set context_attribute to post object
#     context_object_name = "resource_posts"

#     # Add ordering attribute to put most recent post to top
#     ordering = ["-date_created"]

#     # Add pagination
#     paginate_by = 3

#     def get_context_data(self, **kwargs):
#         context = super(MessageListView, self).get_context_data(**kwargs)
#         context["mapbox_access_token"] = "pk." + os.environ.get("MAPBOX_KEY")
#         context["timestamp_now"] = datetime.datetime.now()
#         return context
@login_required
def get_reminders_count(request):
    posts = ReservationPost.objects.filter(
        reservationstatus=1,
        dropoff_time_request__gt=timezone.now(),
        dropoff_time_request__lte=timezone.now() + datetime.timedelta(minutes=10),
    )
    data = posts.count()
    return HttpResponse(data)


@login_required
def get_reminder(request):
    posts = ReservationPost.objects.filter(
        reservationstatus=1,
        dropoff_time_request__gt=timezone.now(),
        dropoff_time_request__lte=timezone.now() + datetime.timedelta(minutes=10),
    )
    messages = []
    for post in posts:
        message = {
            "resource": post.post.title,
            "receiver": post.helpseeker.username,
            "dropofftime": post.dropoff_time_request,
        }
        messages.append(message)
    context = {
        "messages": messages,
    }
    # data = posts.count()
    # print(data)
    return render(request, "donation/messages.html", context)


def donation_expired(request):
    user = request.user
    post_list = ResourcePost.objects.filter(
        donor=user,
        status="EXPIRED",
    ).order_by("-date_created")

    page = request.GET.get("page", 1)
    paginator = Paginator(post_list, 5)
    try:
        expired_donation_posts = paginator.page(page)
    except PageNotAnInteger:
        expired_donation_posts = paginator.page(1)
    except EmptyPage:
        expired_donation_posts = paginator.page(paginator.num_pages)

    context = {
        "expired_donation_posts": expired_donation_posts,
    }
    return render(request, "donation/expired.html", context)
