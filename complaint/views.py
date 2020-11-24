from django.shortcuts import render, redirect
from .forms import ComplaintForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .models import Complaint
from django.urls import reverse


# class ComplaintCreateView(LoginRequiredMixin, CreateView):
#     model = Complaint
#     fields = ["subject", "message", "image", "resource_post"]
#     success_message = "Your complaint has been received. We will look into it."
#
#     def form_valid(self, form):
#         form.instance.issuer = self.request.user
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return redirect('issue-complaint')

def issue_complaint(request):
    if request.method == "POST":
        filled_form = ComplaintForm(request.POST, request.FILES)
        if filled_form.is_valid():
            note = (
                "Your complaint about %s has been received. \
                    We will look into it!!"
                % (filled_form.cleaned_data["subject"],)
            )
            new_form = ComplaintForm
            final_form = filled_form.save(commit=False)
            final_form.issuer = request.user
            if request.user.helpseekerprofile:
                final_form.receiver = final_form.reservation_post.donor
            elif request.user.donorprofile:
                final_form.receiver = final_form.reservation_post.helpseeker
            else: #if admin
                final_form.receiver = final_form.issuer


            final_form.save()
            # filled_form.issuer = request.user
            # print(filled_form.issuer)
            # filled_form.save()
            return render(
                request,
                "complaint/complaint_form.html",
                {"form": new_form, "note": note},
            )
    else:
        form = ComplaintForm()
        return render(
            request, "complaint/complaint_form.html", {"form": form}
        )
