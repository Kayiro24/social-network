from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import CreationModificationBase


class User(AbstractUser, CreationModificationBase):
    class RoleChoice(models.TextChoices):
        ADMIN = 'admin'
        READ = 'read'
        WRITE = 'write'

    email = models.EmailField(db_index=True, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=True, blank=True, default=None)
    role = models.CharField(max_length=10, choices=RoleChoice.choices, default=RoleChoice.ADMIN)

    def get_tokens(self):
        """Returns a tuple of JWT tokens (token, refresh_token)"""
        refresh = RefreshToken.for_user(self)

        return str(refresh.access_token), str(refresh)
