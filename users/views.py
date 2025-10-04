# users/views.py
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import LoginForm, SignUpForm
from .models import User


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("users:login")


class SignInView(LoginView):
    form_class = LoginForm
    template_name = "users/login.html"


class SignOutView(LogoutView):
    next_page = reverse_lazy("users:login")
    http_method_names = ["get", "post", "options"]  # enable GET
