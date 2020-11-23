from django.shortcuts import render
from .forms import ComplaintForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .models import Complaint


class ComplaintCreateView(LoginRequiredMixin, CreateView):
    model = Complaint
    fields = ["subject", "message", "image", "resource_post"]
    success_message = "Your complaint has been received. We will look into it."

    def form_valid(self, form):
        form.instance.issuer = self.request.user
        return super().form_valid(form)

# def issue_complaint(request):
#     if request.method == "POST":
#         filled_form = ComplaintForm(request.POST, request.FILES)
#         if filled_form.is_valid():
#             note = (
#                 Your complaint about %s has been received. \
#                     We will look into it!!
#                 % (filled_form.cleaned_data["subject"],)
#             )
#             new_form = ComplaintForm
#             filled_form.save()
#             return render(
#                 request,
#                 "complaint/issue_complaint.html",
#                 {"complaintform": new_form, "note": note},
#             )
#     else:
#         form = ComplaintForm()
#         return render(
#             request, "complaint/issue_complaint.html", {"complaintform": form}
#         )
#

#
# class PostCreateView(LoginRequiredMixin, CreateView):
#     # Basic create view
#     model = ResourcePost
#     fields = [
#         "title",
#         "image",
#         "description",
#         "quantity",
#         "dropoff_time_1",
#         "dropoff_time_2",
#         "dropoff_time_3",
#         "resource_category",
#         "dropoff_location",
#     ]
#
#     def get_form(self):
#         form = super().get_form()
#         form.fields["dropoff_time_1"].widget = DateTimePickerInput()
#         form.fields["dropoff_time_2"].widget = DateTimePickerInput()
#         form.fields["dropoff_time_3"].widget = DateTimePickerInput()
#         return form
#
#     # Overwrite form valid method
#     def form_valid(self, form):
#         form.instance.donor = self.request.user
#         if (
#             not form.cleaned_data["dropoff_location"]
#             and not form.instance.donor.donorprofile.dropoff_location
#         ):
#             messages.error(self.request, "Please input your dropoff location.")
#             return super().form_invalid(form)
#         return super().form_valid(form)
