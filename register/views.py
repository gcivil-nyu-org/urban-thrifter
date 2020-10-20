from django.shortcuts import render, redirect
from .forms import HelpseekerForm, DonorForm
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

def register(request):
    # Redirect to login page
    return render(request, 'register/index.html')

def helpseeker_register(request):
    if request.user.is_authenticated:
        # Redirect to login page
        return redirect('register:register')
    if request.method == 'POST':
        form = HelpseekerForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            profile = HelpseekerProfile(user=user)
            profile.borough = form.cleaned_data.get('borough')
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
            return HttpResponseRedirect(reverse('register:email_sent'))
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
            return HttpResponseRedirect(reverse('register:email_sent'))
    else:
        form = DonorForm()
    return render(request, 'register/donor_register.html', {'form':form})

def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print(user.username)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()       
        return render(request, 'register/activate_confirmation.html')
    return render(request, 'register/activate_failure.html')
    
def email_sent(request):
    if request.method == 'GET':
        return render(request, 'register/email_sent.html')
