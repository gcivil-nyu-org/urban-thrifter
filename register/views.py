from django.shortcuts import render, redirect, get_object_or_404
import os
from .forms import HelpseekerForm, DonorForm, HelpseekerUpdateForm

# , UserUpdateForm
from .models import HelpseekerProfile, DonorProfile
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from register.token_generator import generate_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.core.exceptions import PermissionDenied
from reservation.models import ReservationPost


def register(request):
    # Redirect to login page
    return render(request, "register/register_main.html")


def helpseeker_register(request):
    if request.user.is_authenticated:
        # Redirect to login page
        return redirect("home")
    if request.method == "POST":
        form = HelpseekerForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            profile = HelpseekerProfile(user=user)
            profile.borough = form.cleaned_data.get("borough")
            resources = form.cleaned_data.get("resource")
            d = {}
            for i in range(0, 3):
                if 0 <= i < len(resources):
                    d["resource{0}".format(i)] = resources[i]
                else:
                    d["resource{0}".format(i)] = None
            profile.rc_1 = d["resource0"]
            profile.rc_2 = d["resource1"]
            profile.rc_3 = d["resource2"]
            profile.save()

            # Email verification

            email_subject = "Activate Your Account!"
            message = render_to_string(
                "register/activate_account.html",
                {
                    "user": user,
                    "domain": os.environ.get("DOMAIN_NAME"),
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": generate_token.make_token(user),
                },
            )
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()

            # Must redirect to login page (this is a placeholder)
            return HttpResponseRedirect(reverse("register:email-sent"))
    else:
        form = HelpseekerForm()
    return render(request, "register/helpseeker_register.html", {"form": form})


def donor_register(request):
    if request.user.is_authenticated:
        # Redirect to login page
        return redirect("home")
    if request.method == "POST":
        form = DonorForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            profile = DonorProfile(user=user)
            profile.save()

            # Email verification

            email_subject = "Activate Your Account!"
            message = render_to_string(
                "register/activate_account.html",
                {
                    "user": user,
                    "domain": os.environ.get("DOMAIN_NAME"),
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": generate_token.make_token(user),
                },
            )
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()

            # Must redirect to login page (this is a placeholder)
            return HttpResponseRedirect(reverse("register:email-sent"))
    else:
        form = DonorForm()
    return render(request, "register/donor_register.html", {"form": form})


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "register/activate_confirmation.html")
    return render(request, "register/activate_failure.html")


def email_sent(request):
    if request.method == "GET":
        return render(request, "register/email_sent.html")


@login_required
def helpseeker_edit_profile(request):
    if request.method == "POST":
        # instance=request.user can prefill the existing information in the form
        hs_form = HelpseekerUpdateForm(
            request.POST, instance=request.user.helpseekerprofile
        )
        # hs_user_form = UserUpdateForm(request.POST, instance=request.user)
        if hs_form.is_valid():
            hs_form.save()
            # hs_user_form.save()
            messages.success(request, "Account updated successfully.")
            return redirect("register:helpseeker-profile")
        else:
            if not hs_form.is_valid():
                messages.warning(request, "Repetitive resource category.")
            # if not hs_user_form.is_valid():
            #     messages.warning(request, "Invalid Email Entry.")
    else:
        hs_form = HelpseekerUpdateForm(instance=request.user.helpseekerprofile)
        # hs_user_form = UserUpdateForm(instance=request.user)

    context = {
        "hs_form": hs_form
        # "hs_user_form": hs_user_form
    }
    return render(request, "register/helpseekerprofile_form.html", context)


class DonorUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DonorProfile
    fields = ["dropoff_location"]
    success_message = "Account updated successfully."

    def get_object(
        self,
    ):
        username = self.kwargs.get("username")
        if not User.objects.filter(username=username):
            raise Http404
        elif username != self.request.user.username:
            raise PermissionDenied
        else:
            return get_object_or_404(
                DonorProfile, user__username__iexact=self.request.user
            )


@login_required
def delete_profile(request):
    # user = request.user
    if DonorProfile.objects.filter(user=request.user):
        reservationposts = ReservationPost.objects.filter(donor=request.user)
    elif HelpseekerProfile.objects.filter(user=request.user):
        reservationposts = ReservationPost.objects.filter(helpseeker=request.user)
    confirmed = 0

    for reservationpost in reservationposts:
        print(reservationpost.post.status)
        if reservationpost.post.status == "RESERVED":
            confirmed += 1
    try:
        if confirmed == 0:
            for reservationpost in reservationposts:
                if (
                    reservationpost.post.status != "CLOSED"
                    and reservationpost.post.status != "RESERVED"
                ):
                    reservationpost.post.status = "AVAILABLE"
                    reservationpost.post.save()
                    print(reservationpost.post.status)
            request.user.delete()
            messages.success(request, "Account deleted successfully.")
            return redirect("/")
        elif confirmed > 0:
            messages.info(
                request,
                "You can not delete your profile because you have "
                + str(confirmed)
                + " confirmed reservation"
                + ("s." if confirmed > 1 else "."),
            )
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            messages.error(
                request, "Your profile deletion was unsuccessful. Please try again!"
            )
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    except Exception:
        messages.error(
            request, "Your profile deletion was unsuccessful. Please try again!"
        )
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def bad_request(request, exception):
    response = render(request, "register/errorpage/error.html")
    response.status_code = 400
    return response


def permission_denied(request, exception):
    response = render(request, "register/errorpage/403_permission_denied.html")
    response.status_code = 403
    return response


def page_not_found(request, exception):
    response = render(request, "register/errorpage/404_page_not_found.html")
    response.status_code = 404
    return response


def server_error(request):
    # print(request)
    response = render(request, "register/errorpage/500_server_error.html")
    response.status_code = 500
    return response


def bad_gateday(request):
    response = render(request, "register/errorpage/502_bad_gateway.html")
    response.status_code = 500
    return response


def error(request, exception):
    return render(request, "register/errorpage/error.html")
