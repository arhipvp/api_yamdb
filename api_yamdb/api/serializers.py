from rest_framework import serializers

from .models import Genres


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genres
        lookup_field = 'slug'