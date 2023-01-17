from django.db import models

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
