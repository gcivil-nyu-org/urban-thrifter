from django import forms
from .models import Helpseeker
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation

BOROUGH_CHOICES=[
    ('Manhattan', 'Manhattan'),
    ('Brooklyn', 'Brooklyn'),
    ('Queens', 'Queens'),
    ('The Bronx', 'The Bronx'),
    ('Staten Island', 'Staten Island'),
]
RESOURCE_CHOICES=[
    ('FOOD', 'Food'),
    ('PPE', 'Personal Protective Equipment'),
    ('CLOTH', 'Clothing And Covers'),
    ('ELEC', 'Electronics')
]

class HelpseekerForm(forms.ModelForm):
    username = forms.CharField(label='Username', min_length=4, max_length=50, required=True)
    email = forms.EmailField(label='Email', max_length=60, required=True)
    password = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirm Password', max_length=30, widget=forms.PasswordInput, required=True)
    borough = forms.CharField(label='Borough', widget=forms.RadioSelect(choices=BOROUGH_CHOICES), required=True)
    resource = forms.MultipleChoiceField(label='Resources (select up to 3)', widget=forms.CheckboxSelectMultiple, choices=RESOURCE_CHOICES, required=False)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        holder = Helpseeker.objects.filter(username=username)
        if holder.count():
            raise ValidationError("Username already exists")
        if not username.isalnum():
            raise ValidationError("Username must contain only letters and numbers")
        return username
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        holder = Helpseeker.objects.filter(email=email)
        if holder.count():
            raise ValidationError("Email already exists")
        return email
    def clean_password2(self):
        password = self.cleaned_data['password']
        password_validation.validate_password(password)
        password2 = self.cleaned_data['password2']
        if password and password2 and password != password2:
            raise ValidationError("Passwords don't match")
        return password2
    def clean_resource(self):
        resource = self.cleaned_data['resource']
        resource_length = len(resource)
        if resource_length > 3:
            raise ValidationError("Select up to 3 resources")
        return resource

    class Meta:
        model = Helpseeker
        fields = ('username', 'email', 'password', 'borough')

    field_order = ['username', 'email', 'password', 'password2', 'borough', 'resource']
        

    
    
