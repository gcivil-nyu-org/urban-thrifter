from django.shortcuts import render
from .forms import ComplaintForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from reservation.models import ReservationPost


@login_required(login_url='/login/')
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
