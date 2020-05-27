from django.db import models


class Genre(models.Model):
    """
    Database Model to store genres, linked with Movies model using
    Many-to-Many relationship
    """
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Movie(models.Model):
    """
    Database Model to store movies, linked with Genre model using
    Many-to-Many relationship
    """
    name = models.CharField(max_length=200)
    director = models.CharField(max_length=50)
    imdb_score = models.DecimalField(max_digits=2, decimal_places=1)
    popularity = models.DecimalField('99popularity', max_digits=3, decimal_places=1)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.name

