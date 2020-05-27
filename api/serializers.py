from .models import Movie, Genre
from rest_framework import serializers


class GenreSerializer(serializers.ModelSerializer):
    """
        The Genre serializer that returns the genre with all its fields.
    """
    class Meta:
        model = Genre
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    """
    The Movie serializer that returns the movie data and also adds the genre data with all its fields.
    """

    # To load the genre data fields
    genres = GenreSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'

    # Custom create function implementation since we have many-to-many relation in our data set
    # New moive is created whilst checking if the genre already exists.
    def create(self, validated_data):
        genre_data = validated_data.pop('genres')
        new_movie = Movie.objects.create(**validated_data)
        genre_ids = []
        for genre in genre_data:
            genre_exits = Genre.objects.filter(**genre)
            if genre_exits.exists():
                genre_ids.append(genre_exits.get().id)
            else:
                new_genre = Genre(**genre)
                new_genre.save()
                genre_ids.append(new_genre.id)

        new_movie.genres.add(*genre_ids)
        return new_movie

    # The id of the genre that is passed in the API is loaded and available here as instance.
    # We update the instance on the with the data provided in the body.
    # Same is used to make partial updates(PATCH)
    def update(self, instance, validated_data):
        genre_data = validated_data.pop('genres', [])
        instance = super().update(instance, validated_data)
        if genre_data:
            instance.genres.clear()
        genre_ids = []
        for genre in genre_data:
            genre_exits = Genre.objects.filter(**genre)
            if genre_exits.exists():
                genre_ids.append(genre_exits.get().id)
            else:
                new_genre = Genre(**genre)
                new_genre.save()
                genre_ids.append(new_genre.id)

        instance.genres.add(*genre_ids)
        return instance


