from django.http import HttpRequest
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator
from reviews.models import Categories, Comment, Genres, Review, Title, User


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }



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
    username = serializers.RegexField(
        "^[\w.@+-]+\Z$", max_length=150,
        required=True, validators=[
            UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class ReviewsSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def get_author(self, request: HttpRequest) -> User:
        del request
        return self.context.get('request').user

    def get_title(self, request: HttpRequest) -> Title:
        del request
        return get_object_or_404(
            Title,
            pk=self.context.get('view').kwargs.get('title_id'),
        )

    def validate(self, data):
        if self.context.get('request').method == 'POST':
            if Review.objects.filter(
                title=self.get_title(self),
                author=self.get_author(self),
            ).exists():
                raise ValidationError(
                    'На одно произведение можно оставить только один отзыв',
                )
        return data

    def create(self, validated_data):
        return Review.objects.create(
            title=self.get_title(self),
            author=self.get_author(self),
            **validated_data,
        )

    class Meta:
        model = Review
        fields = ('author', 'title', 'id', 'text', 'pub_date', 'score')


class CommentsSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def create(self, validated_data):
        return Comment.objects.create(
            review=get_object_or_404(
                Review,
                pk=self.context.get('view').kwargs.get('review_id'),
            ),
            author=self.context.get('request').user,
            **validated_data,
        )

    class Meta:
        model = Comment
        fields = ('author', 'review', 'id', 'text', 'pub_date')

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('score')


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )
    """ score = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    ) """
    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        model = Title
        