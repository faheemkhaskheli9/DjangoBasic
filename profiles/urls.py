# profiles/urls.py
from django.urls import path
from .views import MyProfileView, ProfileUpdateView

app_name = "profiles"

urlpatterns = [
    path("me/", MyProfileView.as_view(), name="me"),
    path("edit/", ProfileUpdateView.as_view(), name="edit"),
]
