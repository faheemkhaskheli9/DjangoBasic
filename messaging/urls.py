# messaging/urls.py
from django.urls import path
from .views import InboxView, ThreadView, NewThreadView, UnreadCountView

app_name = "messaging"

urlpatterns = [
    path("", InboxView.as_view(), name="inbox"),
    path("new/", NewThreadView.as_view(), name="new"),
    path("t/<int:pk>/", ThreadView.as_view(), name="thread"),
    path("unread-count/", UnreadCountView.as_view(), name="unread_count"),
]
