import hashlib

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

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
    username = models.CharField(unique=True, max_length=150, verbose_name='Имя пользователя')
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        max_length=254,
        verbose_name='Электронная почта'
    )
    first_name = models.CharField(blank=True, max_length=150, verbose_name='Имя')
    last_name = models.CharField(blank=True, max_length=150, verbose_name='Фамилия')
    bio = models.TextField(blank=True, verbose_name='Наверное это биография:)')
    role = models.CharField(
        choices=POSSIBLE_ROLES,
        default=USER,
        max_length=10,
        verbose_name='Роль'
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
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Categories(models.Model):
    name = models.CharField(
        max_length=256,
        null=False,
        blank=False,
        verbose_name='Категория'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Slug'
    )
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
class Genre(models.Model):
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
        verbose_name='Slug'
    )
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
    
class Title(models.Model):
    name = models.CharField(
        max_length=256,
        blank=False,
        null=False,
        verbose_name='Название произведения'
    )
    year = models.IntegerField(verbose_name='Гоп производства')
    description = models.TextField(verbose_name='Описание')
    genre = models.ManyToManyField(Genre, related_name='genres', verbose_name='Жанры')
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        null=True,
        related_name='category',
        verbose_name='Категория'
    )
    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'







class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='review author',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='review title',
    )
    text = models.TextField(verbose_name='Текст отзыва')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    score = models.IntegerField(verbose_name='Рейтинг',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review',
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self) -> str:
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    def __str__(self) -> str:
        return self.text
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
