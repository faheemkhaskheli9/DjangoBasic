# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Keep core auth clean; add auth-related flags here (if needed)
    email = models.EmailField(unique=True)

    # Example extra auth field
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.get_username()
