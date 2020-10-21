from django.urls import path
from . import views
from .views import (HelpseekerProfileDetailView)
from django.contrib.auth import views as auth_views

app_name="register"
urlpatterns = [
    path('', views.register, name="register"),
    path('helpseeker', views.helpseeker_register, name="helpseeker_register"),
    path('donor', views.donor_register, name="donor_register"),
    path('activate/<uidb64>/<token>', views.activate_account, name="activate"),
    path('email_sent', views.email_sent, name="email_sent"),
    # path('helpseeker/<int:pk>/edit', HelpseekerUpdateView.as_view(), name='helpseeker_edit'),
    path('helpseeker/edit', views.helpseeker_edit_profile, name='helpseeker_edit'),
    path('helpseeker/profile/', views.helpseeker_edit_profile, name='helpseeker_profile'),
    #path('donor/<int:pk>', HelpseekerProfileDetailView.as_view(), name='donor_profile'),
    path('login/', auth_views.LoginView.as_view(template_name='register/login.html'), name="login"),
    
     # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
