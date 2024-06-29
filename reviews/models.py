from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from movies.models import Movie


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT, related_name='reviews')
    stars = models.IntegerField(
        validators=[
            MinValueValidator(1, 'A avaliacao n pode conter menos de 1 estrelas'),
            MaxValueValidator(5, 'A avaliacao n pode conter mais de 5 estrelas.'),
        ]
    )

    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.movie)
