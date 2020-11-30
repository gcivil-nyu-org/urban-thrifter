from django.shortcuts import render
from .forms import ComplaintForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def issue_complaint(request):
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
            final_form.issuer = request.user

            try:
                if request.user.helpseekerprofile:
                    final_form.receiver = final_form.reservation_post.donor
            except Exception:
                if request.user.donorprofile:
                    final_form.receiver = final_form.reservation_post.helpseeker

            final_form.save()
            return render(request, "complaint/complaint_form.html", {"form": new_form})

    else:
        form = ComplaintForm()
        return render(request, "complaint/complaint_form.html", {"form": form})
