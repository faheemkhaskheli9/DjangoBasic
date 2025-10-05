# messaging/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_message_notifications(sender, instance: Message, created, **kwargs):
    if not created:
        return
    for recipient in instance.recipients():
        Notification.objects.create(user=recipient, message=instance)
