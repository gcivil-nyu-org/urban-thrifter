from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    reservation_function,
)

urlpatterns = [
    path("", PostListView.as_view(), name="reservation-home"),
    # path("new/", PostCreateView.as_view(), name="reservation-new"),
    path("post/<int:pk>", PostDetailView.as_view(), name="reservation-request"),
    path("function/<int:id>", reservation_function, name="reservation-function"),
]
