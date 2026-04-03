from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)