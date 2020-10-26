from django.shortcuts import render, redirect, get_object_or_404
from .forms import HelpseekerForm, DonorForm, HelpseekerUpdateForm
from .models import HelpseekerProfile, DonorProfile
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
import os

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from register.token_generator import generate_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.views.generic import (ListView, CreateView, DetailView, UpdateView)
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404


def register(request):
    # Redirect to login page
    return render(request, 'register/index.html')

def helpseeker_register(request):
    #if request.user.is_authenticated:
        # Redirect to login page
        #return redirect('register:register')
    if request.method == 'POST':
        form = HelpseekerForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            profile = HelpseekerProfile(user=user)
            profile.borough = form.cleaned_data.get('borough')
            resources = form.cleaned_data.get('resource')
            d = {}
            for i in range(0,3):
                if 0 <= i < len(resources):
                    d['resource{0}'.format(i)] = resources[i]
                else:
                    d['resource{0}'.format(i)] = None
            profile.rc_1 = d['resource0']
            profile.rc_2 = d['resource1']
            profile.rc_3 = d['resource2']
            profile.save()

            # Email verification

            email_subject = "Activate Your Account!"
            message = render_to_string('register/activate_account.html',
                {
                'user':user,
                'domain':os.environ.get('DOMAIN_NAME'),
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':generate_token.make_token(user),
                },
            )
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()

            # Must redirect to login page (this is a placeholder)
            return HttpResponseRedirect(reverse('register:email-sent'))
    else:
        form = HelpseekerForm()
    return render(request, 'register/helpseeker_register.html', {'form':form})

def donor_register(request):
    if request.user.is_authenticated:
        # Redirect to login page
        return redirect('register:register')
    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            profile = DonorProfile(user=user)
            profile.save()

            # Email verification

            email_subject = "Activate Your Account!"
            message = render_to_string('register/activate_account.html',
                {
                'user':user,
                'domain':os.environ.get('DOMAIN_NAME'),
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':generate_token.make_token(user),
                },
            )
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()

            # Must redirect to login page (this is a placeholder)
            return HttpResponseRedirect(reverse('register:email-sent'))
    else:
        form = DonorForm()
    return render(request, 'register/donor_register.html', {'form':form})

def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print(user.username)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'register/activate_confirmation.html')
    return render(request, 'register/activate_failure.html')

def email_sent(request):
    if request.method == 'GET':
        return render(request, 'register/email_sent.html')

@login_required
def helpseeker_edit_profile(request):
    if request.method == 'POST':
        # instance=request.user can prefill the existing information in the form
        hs_form = HelpseekerUpdateForm(request.POST, instance=request.user.helpseekerprofile)

        if hs_form.is_valid():
            hs_form.save()
        messages.success(request, f'Account updated successfully.')
        return redirect('register:helpseeker-profile')
    else:
        hs_form = HelpseekerUpdateForm(instance=request.user.helpseekerprofile)

    context = {
        'hs_form': hs_form
    }
    return render(request, 'register/helpseekerprofile_form.html', context)


class DonorUpdateView(LoginRequiredMixin, UpdateView):
    model = DonorProfile
    fields = ['dropoff_location']

    def get_object(self, **kwargs):
        username = self.kwargs.get("username")
        if username is None:
            raise Http404
        return get_object_or_404(DonorProfile, user__username__iexact=username)

# @login_required
# def donor_edit_profile(request):
#     if request.method == 'POST':
#         # instance=request.user can prefill the existing information in the form
#         donor_form = DonorUpdateForm(request.POST, instance=request.user.donorprofile)
#
#         if donor_form.is_valid():
#             donor_form.save()
#         messages.success(request, f'Account updated successfully.')
#         return redirect('register:donor-profile')
#     else:
#         donor_form = DonorUpdateForm(instance=request.user.donorprofile)
#
#     context = {
#         'donor_form': donor_form
#     }
#     return render(request, 'register/donorprofile_form.html', context)
