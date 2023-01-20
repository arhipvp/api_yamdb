from rest_framework import serializers
from reviews.models import Genres, Title, User, Сategories


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = '__all__'
        lookup_field = 'slug'

class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        fields = '__all__'
        model = Title

class СategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Сategories
        fields = ('name', 'slug')
        

class AuthSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')


class AuthTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
