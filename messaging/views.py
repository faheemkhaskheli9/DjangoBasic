# messaging/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages as dj_messages
from django.http import JsonResponse, Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, View
from django.db.models import Q, Max, Count

from django.contrib.auth import get_user_model
from .models import Thread, Message, Notification
from .forms import NewThreadForm, MessageForm

User = get_user_model()

class InboxView(LoginRequiredMixin, ListView):
    template_name = "messaging/inbox.html"
    context_object_name = "threads"

    def get_queryset(self):
        user = self.request.user
        qs = Thread.objects.filter(Q(user_a=user) | Q(user_b=user))
        # annotate last message time & unread count for ordering/display
        qs = qs.annotate(
            last_time=Max("messages__created_at"),
        ).order_by("-last_time", "-created_at")
        return qs

class ThreadView(LoginRequiredMixin, DetailView, FormView):
    template_name = "messaging/thread.html"
    model = Thread
    form_class = MessageForm
    context_object_name = "thread"

    def get_success_url(self):
        return reverse_lazy("messaging:thread", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        thread = super().get_object(queryset)
        user = self.request.user
        if user not in (thread.user_a, thread.user_b):
            raise Http404()
        # mark notifications read for this thread
        Notification.objects.filter(
            user=user, message__thread=thread, is_read=False
        ).update(is_read=True, read_at=None)
        return thread

    def form_valid(self, form):
        thread = self.get_object()
        msg = Message.objects.create(
            thread=thread, sender=self.request.user, body=form.cleaned_data["body"]
        )
        dj_messages.success(self.request, "Message sent.")
        return redirect(self.get_success_url())

class NewThreadView(LoginRequiredMixin, FormView):
    template_name = "messaging/new.html"
    form_class = NewThreadForm

    def get_form_kwargs(self):
        kw = super().get_form_kwargs()
        kw["current_user"] = self.request.user
        return kw

    def form_valid(self, form):
        to_user = form.cleaned_data["to"]
        body = form.cleaned_data["body"]
        thread = Thread.for_users(self.request.user, to_user)
        Message.objects.create(thread=thread, sender=self.request.user, body=body)
        dj_messages.success(self.request, f"Started conversation with {to_user.username}.")
        return redirect("messaging:thread", pk=thread.pk)

class UnreadCountView(LoginRequiredMixin, View):
    def get(self, request):
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return JsonResponse({"unread": count})
