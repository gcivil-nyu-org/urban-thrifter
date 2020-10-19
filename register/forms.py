from django import forms
from django.contrib.auth.models import User
from .models import HelpseekerProfile
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

BOROUGH_CHOICES=[
    ('MAN', 'Manhattan'),
    ('BRK', 'Brooklyn'),
    ('QUN', 'Queens'),
    ('BRX', 'The Bronx'),
    ('STN', 'Staten Island'),
]
RESOURCE_CATEGORY_CHOICES=[
    ('FOOD', 'Food'),
    ('MDCL', 'Medical/ PPE'),
    ('CLTH', 'Clothing/ Covers'),
    ('ELEC', 'Electronics'),
    ('OTHR', 'Others'),
]

class HelpseekerForm(UserCreationForm):
    username = forms.CharField(label='Username', min_length=4, max_length=50, required=True)
    email = forms.EmailField(label='Email', max_length=60, required=True)
    password1 = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirm Password', max_length=30, widget=forms.PasswordInput, required=True)
    borough = forms.CharField(label='Borough', widget=forms.RadioSelect(choices=BOROUGH_CHOICES), required=True)
    resource = forms.MultipleChoiceField(label='Resources (select up to 3)', widget=forms.CheckboxSelectMultiple, choices=RESOURCE_CATEGORY_CHOICES, required=False)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        holder = User.objects.filter(email=email)
        if holder.count():
            raise ValidationError("Email already exists")
        return email
    def clean_resource(self):
        resource = self.cleaned_data['resource']
        resource_length = len(resource)
        if resource_length > 3:
            raise ValidationError("Select up to 3 resources")
        return resource

    class Meta:
        model = User
        fields = ('username', 'password1', 'email')

    field_order = ['username', 'email', 'password1', 'password2', 'borough', 'resource']

# Model form allow you to work with a specific database model
class HelpseekerUpdateForm(forms.ModelForm):
        
    # Keep configuration in one place
    class Meta:
        model = HelpseekerProfile
        # field on the form
        fields = ['borough', 'rc_1', 'rc_2', 'rc_3']
