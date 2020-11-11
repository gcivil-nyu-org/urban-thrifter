from donation.models import ResourcePost
from .models import ReservationPost
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse


# Create your views here.
def home(request):
    return render(request, "reservation/reservation_home.html")


def PostListView(request):
    # Getting posts based on filters or getting all posts
    url_parameter = request.GET.get("q")
    if url_parameter:
        posts = ResourcePost.objects.filter(title__icontains=url_parameter).order_by("-date_created")
    else:
        posts = ResourcePost.objects.all().order_by("-date_created")
        
    # Ajax code
    if request.is_ajax():
        html = render_to_string(
            template_name="reservation/reservation_list.html", 
            context={"posts": posts}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)
        
    return render(request, "reservation/reservation_home.html", {"posts": posts})


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
            reservation.save()
            resource_post.status = "PENDING"
            resource_post.save()
    return redirect("reservation:reservation-confirmation")


# Reservation Detail View


class PostDetailView(DetailView):
    # Basic detail view
    model = ResourcePost
    template_name = "reservation/reservation_request.html"


class ReservationDetailView(DetailView):
    # Basic detail view
    model = ReservationPost
    template_name = "reservation/reservation_detail.html"
