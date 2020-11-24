from django import forms
from django.contrib.auth.models import User
from .models import HelpseekerProfile
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

# from crispy_forms.layout import Layout, Field
# from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper

BOROUGH_CHOICES = [
    ("MAN", "Manhattan"),
    ("BRK", "Brooklyn"),
    ("QUN", "Queens"),
    ("BRX", "Bronx"),
    ("STN", "Staten Island"),
]
RESOURCE_CATEGORY_CHOICES = [
    ("FOOD", "Food"),
    ("MEDICAL/ PPE", "Medical/ PPE"),
    ("CLOTHING/ COVERS", "Clothing/ Covers"),
    ("ELECTRONICS", "Electronics"),
    ("OTHERS", "Others"),
]


class HelpseekerForm(UserCreationForm):
    username = forms.CharField(
        label="",
        min_length=4,
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Username*"}),
    )
    email = forms.EmailField(
        label="",
        max_length=60,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Email*"}),
    )
    password1 = forms.CharField(
        label="",
        max_length=30,
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Password*"}),
    )
    password2 = forms.CharField(
        label="",
        max_length=30,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password*"}),
        required=True,
    )
    borough = forms.CharField(
        label="Borough",
        widget=forms.RadioSelect(choices=BOROUGH_CHOICES),
        required=True,
    )
    resource = forms.MultipleChoiceField(
        label="",
        widget=forms.CheckboxSelectMultiple,
        choices=RESOURCE_CATEGORY_CHOICES,
        required=False,
    )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        holder = User.objects.filter(email=email)
        if holder.count():
            raise ValidationError("Email already exists")
        return email

    def clean_resource(self):
        resource = self.cleaned_data["resource"]
        resource_length = len(resource)
        if resource_length > 3:
            raise ValidationError("Select up to 3 resources")
        return resource

    class Meta:
        model = User
        fields = ("username", "password1", "email")

    field_order = ["username", "email", "password1", "password2", "borough", "resource"]


class DonorForm(UserCreationForm):
    username = forms.CharField(
        label="",
        min_length=4,
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Username*"}),
    )
    email = forms.EmailField(
        label="",
        max_length=60,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Email*"}),
    )
    password1 = forms.CharField(
        label="",
        max_length=30,
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Password*"}),
    )
    password2 = forms.CharField(
        label="",
        max_length=30,
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password*"}),
    )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        holder = User.objects.filter(email=email)
        if holder.count():
            raise ValidationError("Email already exists")
        return email

    class Meta:
        model = User
        fields = ("username", "password1", "email")

    field_order = ["username", "email", "password1", "password2"]


# Model form allow you to work with a specific database model
class HelpseekerUpdateForm(forms.ModelForm):
    # Keep configuration in one place
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False

    def clean(self):
        cleaned_data = super().clean()
        rc_1 = cleaned_data.get("rc_1")
        rc_2 = cleaned_data.get("rc_2")
        rc_3 = cleaned_data.get("rc_3")

        if (
            rc_1 is not None
            and rc_1 in [rc_2, rc_3]
            or rc_2 is not None
            and rc_2 in [rc_1, rc_3]
            or rc_3 is not None
            and rc_3 in [rc_1, rc_2]
        ):
            raise ValidationError("Repetitive resource category")

    class Meta:
        model = HelpseekerProfile
        # field on the form
        fields = ["borough", "rc_1", "rc_2", "rc_3"]
