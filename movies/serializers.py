from django.db.models import Avg
from rest_framework import serializers
from actors.serializers import ActorSerializer
from movies.models import Movie
from genres.serializers import GenreSerializer



class MovieModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'

    def validate_release_date(self, value):
        if value.year < 1950:
            raise serializers.ValidationError('A data do filme nao pode ser menor do que 1990.')
        return value

    def validate_resume(self, value):
        if len(value) > 500:
            raise serializers.ValidationError('resumo nao deve ser maior que 200 caracteres.')
        return value


class MovieListDetailSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True)
    genre = GenreSerializer()
    rate = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'genre', 'actors', 'release_date', 'rate', 'resume']

    def get_rate(self, obj):
        rate = obj.reviews.aggregate(Avg('stars'))['stars__avg']
        if rate:
            return round(rate, 1)
        return None


class MovieStatsSerializer(serializers.Serializer):
    total_movies = serializers.ImageField()
    movies_by_genre = serializers.ListField()
    total_reviews = serializers.IntegerField()
    everage_stars = serializers.FloatField()
