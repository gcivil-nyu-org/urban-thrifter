from django import forms
from .models import Complaint
from django.contrib.auth.models import User


class ComplaintForm(forms.ModelForm):

    class Meta:
        model = Complaint
        fields = ["subject", "message", "image", "reservation_post"]
