# profiles/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from .models import Profile
from .forms import ProfileForm

class MyProfileView(LoginRequiredMixin, DetailView):
    template_name = "profiles/me.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return self.request.user.profile

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "profiles/edit.html"
    success_url = reverse_lazy("profiles:me")

    def get_object(self, queryset=None):
        return self.request.user.profile
