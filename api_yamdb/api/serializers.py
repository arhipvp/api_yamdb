from rest_framework import serializers

from reviews.models import Genres
from reviews.models import User


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genres
        lookup_field = 'slug'


class AuthSignupSerializer(serializers.ModelSerializer):
    username = serializers.RegexField("^[\w.@+-]+\Z$", max_length=150)
    email = serializers.EmailField(required=True, max_length=254)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Использовано недопустимое имя пользователя'
            )
        email_user = User.objects.filter(email=data['email']).first()
        username_user = User.objects.filter(username=data['username']).first()

        if email_user and email_user.username != data['username']:
            raise serializers.ValidationError(
                'Email и username не соответствуют'
            )
        if username_user and username_user.email != data['email']:
            raise serializers.ValidationError(
                'Email и username не соответствуют'
            )
        return data


class AuthTokenSerializer(serializers.ModelSerializer):
    username = serializers.RegexField("^[\w.@+-]+\Z$", max_length=150)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class UsersSerializer(serializers.ModelSerializer):
    username = serializers.RegexField("^[\w.@+-]+\Z$", max_length=150)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
