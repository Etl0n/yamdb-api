from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from users.models import User

from .validators import validate_year

TEXT_LIMIT = 15
LEN_VIEW_REW_COM = 10


class Genre(models.Model):
    name = models.CharField(
        'Наименование жанра',
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='сл_Жанр',
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='сл_Категория',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=256,
    )
    year = models.PositiveSmallIntegerField(
        'Год издания',
        validators=(validate_year,),
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        Genre,
        blank=False,
        related_name='titles',
        verbose_name='Жанр',
    )
    description = models.CharField(
        'Описание',
        max_length=100,
        blank=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.CharField(
        'Текст',
        max_length=200,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[
            MinValueValidator(settings.MIN_SCORE),
            MaxValueValidator(settings.MAX_SCORE),
        ],
    )
    pub_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
    )

    def __str__(self):
        return self.text[:LEN_VIEW_REW_COM:]

    class Meta:
        constraints = [
            UniqueConstraint(
                name='unique_score_for_title', fields=['author', 'title']
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.CharField(max_length=200, verbose_name='Текст')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:LEN_VIEW_REW_COM:]
