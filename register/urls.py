from django.urls import path
from . import views

app_name="register"
urlpatterns = [
    path('', views.register, name="register"),
    path('helpseeker_register', views.helpseeker_register, name="helpseeker_register"),
    path('donor_register', views.donor_register, name="donor_register"),
]
