from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

BOROUGH_CHOICES=[
    ('MAN', 'Manhattan'),
    ('BRK', 'Brooklyn'),
    ('QUN', 'Queens'),
    ('BRX', 'The Bronx'),
    ('STN', 'Staten Island'),
]

class HelpseekerForm(UserCreationForm):
    username = forms.CharField(label='Username', min_length=4, max_length=50, required=True)
    email = forms.EmailField(label='Email', max_length=60, required=True)
    password1 = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirm Password', max_length=30, widget=forms.PasswordInput, required=True)
    borough = forms.CharField(label='Borough', widget=forms.RadioSelect(choices=BOROUGH_CHOICES), required=True)   

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        holder = User.objects.filter(email=email)
        if holder.count():
            raise ValidationError("Email already exists")
        return email

    class Meta:
        model = User
        fields = ('username', 'password1', 'email')

    field_order = ['username', 'email', 'password1', 'password2', 'borough']

class DonorForm(UserCreationForm):
    username = forms.CharField(label='Username', min_length=4, max_length=50, required=True)
    email = forms.EmailField(label='Email', max_length=60, required=True)
    password1 = forms.CharField(label='Password', max_length=30, widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirm Password', max_length=30, widget=forms.PasswordInput, required=True)
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        holder = User.objects.filter(email=email)
        if holder.count():
            raise ValidationError("Email already exists")
        return email

    class Meta:
        model = User
        fields = ('username', 'password1', 'email')

    field_order = ['username', 'email', 'password1', 'password2']
