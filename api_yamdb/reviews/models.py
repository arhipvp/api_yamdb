from django.contrib.auth.models import AbstractUser
from django.db import models

# possible user roles in application
POSSIBLE_ROLES = [
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin')
]


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=150)
    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(blank=True, max_length=150)
    last_name = models.CharField(blank=True, max_length=150)
    bio = models.TextField(blank=True)
    role = models.CharField(
        choices=POSSIBLE_ROLES,
        default='user',
        max_length=10
    )
    confirmation_code = models.CharField(
        max_length=255,
        null=True,
        blank=False,
        default='-'
    )

    def __str__(self):
        return self.username
