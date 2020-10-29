from django.urls import path
from . import views
from .views import PostListView, PostDetailView

urlpatterns = [
    path("", PostListView.as_view(), name="reservation-home"),
    # path("new/", PostCreateView.as_view(), name="reservation-new"),
    path("post/<int:pk>", PostDetailView.as_view(), name="reservation-request"),
]
