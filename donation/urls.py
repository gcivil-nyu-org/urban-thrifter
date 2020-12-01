from django.urls import path
from . import views
from .views import (
    PostCreateView,
    PostListView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
)
import reservation.views as reservation_views

urlpatterns = [
    path("", views.home, name="donation-home"),
    path("all/", PostListView.as_view(), name="donation-all"),
    path("new/", PostCreateView.as_view(), name="donation-new"),
    path("post/<int:pk>", PostDetailView.as_view(), name="donation-detail"),
    path("post/<int:pk>/update", PostUpdateView.as_view(), name="donation-update"),
    path("post/<int:pk>/delete", PostDeleteView.as_view(), name="donation-delete"),
    path("ajax/getResourcePosts", views.get_resource_post, name="get-resource-post"),
    path(
        "notifications/", reservation_views.show_notifications, name="donation-messages"
    ),
]
