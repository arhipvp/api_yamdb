import hashlib

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from .validations import ValidateYear

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
    email = models.EmailField(unique=True, blank=False, null=False, max_length=254)
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


class Categories(models.Model):
    name = models.CharField(
        max_length=256,
        null=False,
        blank=False,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        blank=False,
        null=False,
    )
    year = models.IntegerField(
        validators=[ValidateYear]
    )
    description = models.TextField()
    genre = models.ManyToManyField(Genres, related_name='genres')
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        null=True,
        related_name='category',
    )


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True,
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        UniqueConstraint(
            fields=['author', 'title'],
            name='unique_review',
        )

    def __str__(self) -> str:
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    def __str__(self) -> str:
        return self.text
