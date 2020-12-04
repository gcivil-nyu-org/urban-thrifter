from django.shortcuts import render, redirect
from .forms import ComplaintForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from reservation.models import ReservationPost
from .models import Complaint
from register.models import HelpseekerProfile, DonorProfile


@login_required
def complaint_portal(request):
    user = request.user
    if user.is_authenticated and user.is_superuser:
        complaint_post = Complaint.objects.filter(
            status__in=["PENDING", "Pending"]
        )
        helpseeker_profile_warning = HelpseekerProfile.objects.filter(
            complaint_count=2
        )
        helpseeker_profile_deactivate = HelpseekerProfile.objects.filter(
            complaint_count=3
        )
        donor_profile_warning = DonorProfile.objects.filter(
            complaint_count=2
        )
        donor_profile_deactivate = DonorProfile.objects.filter(
            complaint_count=3
        )
        print(Complaint.objects.all())
        context_complaint = {
            "complaint_posts": complaint_post,
            "hs_warning":helpseeker_profile_warning,
            "hs_deactivate":helpseeker_profile_deactivate,
            "donor_warning":donor_profile_warning,
            "donor_deactivate":donor_profile_deactivate,
        }
        return render(
            request, "complaint/complaint_portal.html", context=context_complaint
        )
    else:
        return redirect("home")


@login_required
def issue_complaint(request, **kwargs):
    user = request.user
    reservation_post = ReservationPost.objects.get(id=kwargs["pk"])

    if user == reservation_post.donor or user == reservation_post.helpseeker:
        if request.method == "POST":
            filled_form = ComplaintForm(request.POST, request.FILES)
            if filled_form.is_valid():
                messages.success(
                    request,
                    'Your complaint about "%s" has been received. \
                            We will look into it.'
                    % (filled_form.cleaned_data["subject"]),
                )

                new_form = ComplaintForm
                final_form = filled_form.save(commit=False)
                final_form.issuer = user
                final_form.reservation_post = reservation_post

                try:
                    if user.helpseekerprofile:
                        final_form.receiver = final_form.reservation_post.donor
                except Exception:
                    if user.donorprofile:
                        final_form.receiver = final_form.reservation_post.helpseeker

                final_form.save()
                return render(
                    request, "complaint/complaint_form.html", {"form": new_form}
                )

        else:
            form = ComplaintForm()
            return render(request, "complaint/complaint_form.html", {"form": form})
    else:
        messages.warning(request, "Not an authorized user to enter this page.")
        return render(request, "complaint/wrong_user.html")
