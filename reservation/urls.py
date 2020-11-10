from django.urls import path
from . import views
from .views import (
    PostDetailView,
    ReservationDetailView,
    reservation_function,
)

urlpatterns = [
    path("confirmed/", views.confirmation, name="reservation-confirmation"),
    path("", views.PostListView, name="reservation-home"),
    # path("new/", PostCreateView.as_view(), name="reservation-new"),
    path("post/<int:pk>", PostDetailView.as_view(), name="reservation-request"),
    path("detail/<int:pk>", ReservationDetailView.as_view(), name="reservation-detail"),
    path("function/<int:id>", reservation_function, name="reservation-function"),
]
