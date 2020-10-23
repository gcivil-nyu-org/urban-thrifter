from django.shortcuts import render

# from django.http import HttpResponse
# from django.contrib import messages
# from django.conf import settings
from django.views.generic import ListView, CreateView, DetailView
from .models import ResourcePost

# , User
from bootstrap_datepicker_plus import DateTimePickerInput
from django.contrib.auth.mixins import LoginRequiredMixin

# , UserPassesTestMixin


# Create your views here.
def home(request):
    context = {"posts": ResourcePost.objects.all()}

    # context is the argument pass into the html
    return render(request, "donation/home.html", context)


# All Donations View
class PostListView(ListView):
    # Basic list view
    model = ResourcePost
    # Assign tempalte otherwise it would look for post_list.html
    # as default template
    template_name = "donation/home.html"

    # Set context_attribute to post object
    context_object_name = "posts"

    # Add ordering attribute to put most recent post to top
    ordering = ["-date_created"]

    # Add pagination
    paginate_by = 5


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
        "dropoff_location",
        "resource_category",
    ]

    def get_form(self):
        form = super().get_form()
        form.fields["dropoff_time_1"].widget = DateTimePickerInput()
        form.fields["dropoff_time_2"].widget = DateTimePickerInput()
        form.fields["dropoff_time_3"].widget = DateTimePickerInput()
        return form

    # Overwrite form valid method
    # def form_valid(self, form):
    #    form.instance.author = self.request.user
    #    return super().form_valid(form)


# Donation Detail View
class PostDetailView(DetailView):
    # Basic detail view
    model = ResourcePost
