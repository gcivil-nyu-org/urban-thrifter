from django.urls import path
from . import views
from .views import (
    PostDetailView,
    ReservationDetailView,
    NotificationCheck,
)
import reservation.views as reservation_views

urlpatterns = [
    path("confirmed/", views.confirmation, name="reservation-confirmation"),
    path("", views.donation_post_list, name="reservation-home"),
    # path("new/", PostCreateView.as_view(), name="reservation-new"),
    path("post/<int:pk>", PostDetailView.as_view(), name="reservation-request"),
    path("detail/<int:pk>", ReservationDetailView.as_view(), name="reservation-detail"),
    path("function/<int:id>", views.reservation_function, name="reservation-function"),
    path("notification/", views.show_notifications, name="reservation-notification"),
    path(
        "notificationpost/<int:id>",
        views.confirm_notification,
        name="confirm-notification",
    ),
    path("ajax_notification/", NotificationCheck.as_view(), name="ajax-notification"),
    path("messages/", reservation_views.helpseeker_notifications, name="donation-messages"),
]
