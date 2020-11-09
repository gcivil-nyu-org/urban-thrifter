from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    ReservationDetailView,
    reservation_function,
    ShowNotifications,
    confirmNotification,
)

urlpatterns = [
    path("confirmed/", views.confirmation, name="reservation-confirmation"),
    path("", PostListView.as_view(), name="reservation-home"),
    # path("new/", PostCreateView.as_view(), name="reservation-new"),
    path("post/<int:pk>", PostDetailView.as_view(), name="reservation-request"),
    path("detail/<int:pk>", ReservationDetailView.as_view(), name="reservation-detail"),
    path("function/<int:id>", reservation_function, name="reservation-function"),
    path("notification/", ShowNotifications, name="reservation-notification"),
    path("notificationpost/<int:id>", confirmNotification, name="confirm-notification"),
]
