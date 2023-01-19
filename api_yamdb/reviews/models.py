import hashlib

from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

# possible user roles in application
POSSIBLE_ROLES = [
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN)
]


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=150)
    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(blank=True, max_length=150)
    last_name = models.CharField(blank=True, max_length=150)
    bio = models.TextField(blank=True)
    role = models.CharField(
        choices=POSSIBLE_ROLES,
        default=USER,
        max_length=10
    )

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def confirmation_code(self):
        return hashlib.md5(self.username.encode()).hexdigest()


class Genres(models.Model):
    name = models.CharField(
        max_length=128,
        unique=True,
        blank=False,
        verbose_name='Жанр',
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        max_length=50,
    )
