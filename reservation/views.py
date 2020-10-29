from django.shortcuts import render
from donation.models import ResourcePost
from .models import ReservationPost
from django.views.generic import ListView, DetailView

# Create your views here.
# All Resource View


# Reservation List View
class PostListView(ListView):
    # Basic list view
    model = ResourcePost
    # Assign tempalte otherwise it would look for post_list.html
    # as default template
    template_name = "reservation/listing_all.html"

    # Set context_attribute to post object
    context_object_name = "posts"

    # Add ordering attribute to put most recent post to top
    ordering = ["-date_created"]

    # Add pagination
    paginate_by = 5


# Reservation Detail View
class PostDetailView(DetailView):
    # Basic detail view
    model = ResourcePost
    template_name = "reservation/reservation_request.html"

class ReservationDetailView(DetailView):
    model = ReservationPost
    template_name = "reservation/reservation_detail.html"
