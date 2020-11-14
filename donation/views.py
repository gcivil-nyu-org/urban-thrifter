from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView
from .models import ResourcePost, User
from bootstrap_datepicker_plus import DateTimePickerInput
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages
import os
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# , UserPassesTestMixin


# Create your views here.


def homepage(request):
    # Redirect to login page
    return render(request, "donation/homepage.html")

def home(request):
    user = request.user
    post_list = ResourcePost.objects.filter(donor=user)
    # .order_by("-date_created")

    page = request.GET.get("page", 1)
    paginator = Paginator(post_list, 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    user = request.user
    context = {"posts": posts}

    return render(request, "donation/reservation_status_nav.html", context)


# All Donations View
class PostListView(ListView):
    # Basic list view
    model = ResourcePost
    # Assign tempalte otherwise it would look for post_list.html
    # as default template
    template_name = "donation/reservation_status_nav.html"

    # Set context_attribute to post object
    context_object_name = "posts"

    # Add ordering attribute to put most recent post to top
    ordering = ["-date_created"]

    # Add pagination
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return ResourcePost.objects.filter(author=user).order_by("-date_created")


# Post Donation View
class PostCreateView(LoginRequiredMixin, CreateView):
    # Basic create view
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
        form = super().get_form()
        form.fields["dropoff_time_1"].widget = DateTimePickerInput()
        form.fields["dropoff_time_2"].widget = DateTimePickerInput()
        form.fields["dropoff_time_3"].widget = DateTimePickerInput()
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
        return super().form_valid(form)


# Donation Detail View
class PostDetailView(DetailView):
    # Basic detail view
    model = ResourcePost


def getResourcePost(request):
    curr_user_rc_1 = request.user.helpseekerprofile.rc_1
    curr_user_rc_2 = request.user.helpseekerprofile.rc_2
    curr_user_rc_3 = request.user.helpseekerprofile.rc_3

    posts = ResourcePost.objects.all()
    passingList = []
    for post in posts:
        if (
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

# funciton based view version of messagelistview
def message_list_view(request):
    post_list = ResourcePost.objects.all().order_by("-date_created")

    page = request.GET.get("page", 1)
    paginator = Paginator(post_list, 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    # if request.method == 'GET':
    timestamp_now = datetime.datetime.now()
    context = {
        "mapbox_access_token": "pk." + os.environ.get("MAPBOX_KEY"),
        "timestamp": timestamp_now,
        "posts": posts,
    }
    return render(request, "donation/messages_home.html", context)