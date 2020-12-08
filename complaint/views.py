from django.shortcuts import render, redirect
from .forms import ComplaintForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from reservation.models import ReservationPost
from .models import Complaint
from register.models import HelpseekerProfile, DonorProfile
from django.contrib.auth.models import User

@login_required
def complaint_portal(request):
    user = request.user
    if user.is_authenticated and user.is_superuser:
        complaint_posts_pending = Complaint.objects.filter(
            status__in=["PENDING", "Pending"]
        )
        complaint_posts_resolved = Complaint.objects.exclude(
            status__in=["PENDING", "Pending"]
        )
        helpseeker_profile_warning = HelpseekerProfile.objects.filter(complaint_count=2)
        helpseeker_profile_deactivate = HelpseekerProfile.objects.filter(
            complaint_count__gte=3
        )
        donor_profile_warning = DonorProfile.objects.filter(complaint_count=2)
        donor_profile_deactivate = DonorProfile.objects.filter(complaint_count__gte=3)
        # print(Complaint.objects.all())
        context_complaint = {
            "complaint_posts_pending": complaint_posts_pending,
            "complaint_posts_resolved": complaint_posts_resolved,
            "hs_warning": helpseeker_profile_warning,
            "hs_deactivate": helpseeker_profile_deactivate,
            "donor_warning": donor_profile_warning,
            "donor_deactivate": donor_profile_deactivate,
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


@login_required
def deactivate_helpseeker(request, **kwargs):
    # user = request.user
    helpseeker_profile = User.objects.get(id=kwargs["pk"])
    try:
        helpseeker_profile.is_active = False
        helpseeker_profile.save()
    except Exception:
        messages.error(request, "User deactivation was unsuccessful. Please try again!")
    # print(user)
    # print("helpseeker_profile: ", helpseeker_profile)
    return redirect("complaint")


@login_required
def complaint_decision(request, **kwargs):
    if request.method == "POST":
        complaint = Complaint.objects.get(id=kwargs["pk"])
        complaint_receiver = User.objects.get(username=complaint.receiver.username)
    if "valid" in request.POST:
        complaint.status = "VALID"
        complaint.save()
        hs_profile = HelpseekerProfile.objects.filter(user_id=complaint_receiver.id)
        donor_profile = DonorProfile.objects.filter(user_id=complaint_receiver.id)
        if donor_profile:
            donor = DonorProfile.objects.get(user_id=complaint_receiver.id)
            donor.complaint_count += 1
            donor.save()
        elif hs_profile:
            helpseeker = HelpseekerProfile.objects.get(user_id=complaint_receiver.id)
            helpseeker.complaint_count += 1
            helpseeker.save()
    elif "invalid" in request.POST:
        complaint.status = "INVALID"
        complaint.save()
    return redirect("complaint")
