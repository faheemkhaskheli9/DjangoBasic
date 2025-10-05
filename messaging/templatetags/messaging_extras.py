# messaging/templatetags/messaging_extras.py
from django import template
from ..models import Notification

register = template.Library()

@register.simple_tag
def other_user(thread, me):
    """Return the other participant in a two-user thread."""
    return thread.user_b if thread.user_a_id == me.id else thread.user_a

@register.filter
def is_me(user_obj, me):
    """True if the user_obj is the current user (by id)."""
    try:
        return user_obj.id == me.id
    except Exception:
        return False


@register.simple_tag
def unread_for(thread, me):
    return Notification.objects.filter(
        user=me, message__thread=thread, is_read=False
    ).count()
