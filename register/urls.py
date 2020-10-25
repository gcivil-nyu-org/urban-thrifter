from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "register"
urlpatterns = [
    path("", views.register, name="register"),
    path("helpseeker", views.helpseeker_register, name="helpseeker_register"),
    path("donor", views.donor_register, name="donor_register"),
    path("activate/<uidb64>/<token>", views.activate_account, name="activate"),
    path("email_sent", views.email_sent, name="email_sent"),
    path(
        "helpseeker/profile/", views.helpseeker_edit_profile, name="helpseeker_profile"
    ),
]
