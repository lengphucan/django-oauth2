from django.contrib.auth.models import AbstractUser
from django.db import models


class TimestampsModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, TimestampsModel):
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name="Email Address",
        help_text="User's email address.",
        error_messages={"unique": "error_email_exists"},
    )
    username = models.CharField(
        max_length=64,
        unique=True,
        verbose_name="Username",
        help_text="User's username.",
        error_messages={"unique": "error_username_exists"},
    )
    password = models.CharField(
        max_length=255,
        null=True,
        verbose_name="Password",
        help_text="Encrypted password of the user.",
    )
    balance = models.PositiveIntegerField(
        default=0, verbose_name="Balance", help_text="User's current balance."
    )
