from rest_framework import serializers

from reviews.models import Genres, User, Title, Сategories



class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genres
        lookup_field = 'slug'

class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Title

class СategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Сategories

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
