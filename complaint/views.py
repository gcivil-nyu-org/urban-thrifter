from django.shortcuts import render, redirect
from .forms import ComplaintForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .models import Complaint
from donation.models import ResourcePost
from django.urls import reverse

@login_required
def issue_complaint(request, **kwargs):

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
            final_form.reservation_post = ResourcePost.objects.get(id=kwargs['pk'])

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


# class ComplaintCreateView(LoginRequiredMixin, CreateView):	
#     model = Complaint	
#     fields = ["subject", "message", "image"]	
#     success_message = "Your complaint has been received. We will look into it."	
	
#     def form_valid(self, form):	
#         form.instance.issuer = self.request.user	
#         return super().form_valid(form)	
	
#     def get_success_url(self):	
#         return redirect('issue-complaint')

#     def get_context_data(self, **kwargs):
#         context = super(ComplaintCreateView, self).get_context_data(**kwargs)
#         return context