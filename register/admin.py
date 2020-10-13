from django.contrib import admin
from .models import HelpseekerProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class MyUserAdmin(UserAdmin):
    list_display = ("id", "username", "password", "email", "is_active","date_joined", "last_login")

# Register your models here.
admin.site.register(HelpseekerProfile)
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
