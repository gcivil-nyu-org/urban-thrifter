from django.urls import path
from . import views
from .views import PostListView, PostDetailView, ReservationDetailView

urlpatterns = [
    path("", PostListView.as_view(), name="reservation-home"),
    # path("new/", PostCreateView.as_view(), name="reservation-new"),
    path("post/<int:pk>", PostDetailView.as_view(), name="reservation-request"),
    path("reservation/<int:pk>", ReservationDetailView.as_view(), name="reservation-detail"),
]
