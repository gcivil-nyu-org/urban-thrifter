from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView
from .models import ResourcePost, User
from bootstrap_datepicker_plus import DateTimePickerInput
from django.contrib.auth.mixins import LoginRequiredMixin

# , UserPassesTestMixin


# Create your views here.


def homepage(request):
    # Redirect to login page
    return render(request, "donation/homepage.html")


def home(request):
    user = request.user
    context = {"posts": ResourcePost.objects.filter(donor=user)}

    # context is the argument pass into the html

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
        return super().form_valid(form)


# Donation Detail View
class PostDetailView(DetailView):
    # Basic detail view
    model = ResourcePost
