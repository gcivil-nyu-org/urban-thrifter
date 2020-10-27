from django.urls import path
from . import views

urlpatterns = [
    path("", views.main_map, name="main_map"),
]
