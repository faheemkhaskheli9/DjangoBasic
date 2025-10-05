# messaging/models.py
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Thread(models.Model):
    user_a = models.ForeignKey(User, related_name="thread_as_a", on_delete=models.CASCADE)
    user_b = models.ForeignKey(User, related_name="thread_as_b", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user_a", "user_b"], name="unique_thread_pair"),
        ]

    def save(self, *args, **kwargs):
        # enforce ordering (a.id < b.id) so uniqueness works
        if self.user_a_id and self.user_b_id and self.user_a_id > self.user_b_id:
            self.user_a, self.user_b = self.user_b, self.user_a
        super().save(*args, **kwargs)

    @staticmethod
    def for_users(u1, u2):
        a, b = (u1, u2) if u1.id < u2.id else (u2, u1)
        thread, _ = Thread.objects.get_or_create(user_a=a, user_b=b)
        return thread

    def other(self, user):
        return self.user_b if user == self.user_a else self.user_a

    def last_message(self):
        return self.messages.order_by("-created_at").first()

    def unread_count_for(self, user):
        return self.notifications.filter(user=user, is_read=False).count()


class Message(models.Model):
    thread = models.ForeignKey(Thread, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def recipients(self):
        # everyone in thread except sender
        return [u for u in (self.thread.user_a, self.thread.user_b) if u_id(u) != self.sender_id]


def u_id(u):
    return getattr(u, "id", u)


class Notification(models.Model):
    user = models.ForeignKey(User, related_name="message_notifications", on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name="notifications", on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    def mark_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=["is_read", "read_at"])
