from django.urls import path
from . import views
from .views import DonorUpdateView

app_name = "register"
urlpatterns = [
    path("", views.register, name="register"),
    path("helpseeker", views.helpseeker_register, name="helpseeker-register"),
    path("donor", views.donor_register, name="donor-register"),
    path("activate/<uidb64>/<token>", views.activate_account, name="activate"),
    path("email-sent", views.email_sent, name="email-sent"),
    path(
        "helpseeker/profile/", views.helpseeker_edit_profile, name="helpseeker-profile"
    ),
    path(
        "donor/profile/<str:username>", DonorUpdateView.as_view(), name="donor-profile"
    ),
    path("delete/", views.delete_profile, name="user-delete"),
]
