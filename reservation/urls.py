from django.urls import path
from . import views
from .views import (
    PostDetailView,
    ReservationDetailView,
    ReservationUpdateView,
    NotificationCheck,
)
import reservation.views as reservation_views

urlpatterns = [
    path("confirmed/", views.confirmation, name="reservation-confirmation"),
    path("", views.donation_post_list, name="reservation-home"),
    path("post/<int:pk>", PostDetailView.as_view(), name="reservation-request"),
    path("detail/<int:pk>", ReservationDetailView.as_view(), name="reservation-detail"),
    path("update/<int:pk>", ReservationUpdateView.as_view(), name="reservation-update"),
    path(
        "update/request/<int:pk>",
        views.reservation_update,
        name="reservation-update-request",
    ),
    path("function/<int:id>", views.reservation_function, name="reservation-function"),
    path("notification/", views.show_notifications, name="reservation-notification"),
    path(
        "notificationpost/<int:id>",
        views.confirm_notification,
        name="confirm-notification",
    ),
    path("ajax_notification/", NotificationCheck.as_view(), name="ajax-notification"),
    path(
        "messages/",
        reservation_views.helpseeker_notifications,
        name="reservation-messages",
    ),
    path(
        "message/<int:id>",
        views.read_message,
        name="read-message",
    ),
]
