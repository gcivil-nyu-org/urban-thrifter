"""urban_thrifter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from complaint import views
from register import views as user_view

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('donation/', include('donation.urls')),
    path('admin/', admin.site.urls),
    path('map/', include('map.urls')),
    path('', user_view.register, name='home'),
    path('issue-complaint/', views.issue_complaint, name='issue-complaint'),
    path('register/', include('register.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='register/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='register/logout.html'), name='logout'),

    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='register/password_reset.html'
         ),
         name='password-reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='register/password_reset_done.html'
         ),
         name='password-reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='register/password_reset_confirm.html'
         ),
         name='password-reset-confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='register/password_reset_complete.html'
         ),
         name='password-reset-complete'),
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
