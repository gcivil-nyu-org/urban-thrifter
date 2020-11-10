from django.urls import path
from . import views
from .views import PostCreateView, PostListView, PostDetailView

urlpatterns = [
    path("", views.home, name="donation-home"),
    path("all/", PostListView.as_view(), name="donation-all"),
    path("new/", PostCreateView.as_view(), name="donation-new"),
    path("post/<int:pk>", PostDetailView.as_view(), name="donation-detail"),
    path('ajax/getResourcePosts', views.getResourcePost, name="getResourcePosts"),
]
