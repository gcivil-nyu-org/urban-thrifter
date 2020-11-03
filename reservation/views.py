from donation.models import ResourcePost
from .models import ReservationPost
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.contrib.auth.models import User
import datetime

# Create your views here.
def reservation_function(request, id):
    if request.method == "POST":
       selected_time = request.POST.get("dropoff_time")
       resource_post = ResourcePost.objects.get(id=id)
       donor_id = User.objects.get(id=resource_post.donor_id)
       helpseeker_id = request.user
       reservation = ReservationPost(dropoff_time_request=selected_time, post=resource_post, donor=donor_id, helpseeker=helpseeker_id)
       reservation.save()
    return redirect("reservation-home")
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
    
