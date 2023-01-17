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

    def __str__(self) -> str:
        return self.text

