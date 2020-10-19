from django.urls import path
from . import views
from .views import (HelpseekerProfileDetailView, HelpseekerUpdateView)
app_name="register"
urlpatterns = [
    path('', views.register, name="register"),
    path('helpseeker', views.helpseeker_register, name="helpseeker_register"),
    path('donor', views.donor_register, name="donor_register"),
    path('activate/<uidb64>/<token>', views.activate_account, name="activate"),
    path('email_sent', views.email_sent, name="email_sent"),
    # path('helpseeker/<int:pk>/edit', HelpseekerUpdateView.as_view(), name='helpseeker_edit'),
    path('helpseeker/edit', views.helpseeker_edit_profile, name='helpseeker_edit'),
    path('helpseeker/<int:pk>', HelpseekerProfileDetailView.as_view(), name='helpseeker_profile'),
]
