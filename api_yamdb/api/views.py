from django.core.mail import send_mail
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework import filters, viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Genres, Title, User, Categories, Review
from rest_framework.decorators import action
from .serializers import (AuthSignupSerializer, AuthTokenSerializer,
                          GenresSerializer, TitleSerializer, UsersSerializer,
                          CategoriesSerializer, ReviewsSerializer,
                          CommentsSerializer, ReadOnlyTitleSerializer)

from .permissions import (
    IsAdminOrReadOnly,
    IsAdminOrSuperUser,
    IsAuthorOrModeratorOrAdminOrSuperuser,
)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(
        methods=['post'],
        detail=False,
        permission_classes=(IsAdminOrSuperUser,)
    )
    def CategoryPost(self, request):
        serializer = CategoriesSerializer(request.data)
        if serializer.is_valid:
            serializer.save()
        return Response(serializer.data)


class AuthSignup(APIView):
    """
    Зарегистрироваmь пользователя и отправить ему код подтверждения на email
    """

    @staticmethod
    def post(request):
        serializer = AuthSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = User.objects.get_or_create(
            username=serializer.data['username'],
            email=serializer.data['email'],
        )
        send_mail(
            'Код подтверждения для yamdb',
            f'Ваш код подтверждения - {user.confirmation_code}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthToken(APIView):
    """Получить JWT-токен"""

    @staticmethod
    def post(request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, username=data['username'])
        if user.confirmation_code != data['confirmation_code']:
            return Response(
                {'confirmation_code': 'Неверный код подтверждения'},
                status=status.HTTP_400_BAD_REQUEST
            )
        token = RefreshToken.for_user(user).access_token
        return Response({'token': str(token)},
                        status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAuthenticated, IsAdminOrSuperUser,)
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def me_actions(self, request):
        """ Получить/Обновить свои данные"""
        if request.method == 'GET':
            serializer = UsersSerializer(request.user)
            return Response(serializer.data)

        serializer = UsersSerializer(
            request.user, data=request.data, partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data)


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = (IsAuthorOrModeratorOrAdminOrSuperuser, )

    def get_queryset(self) -> QuerySet:
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.select_related('title')


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthorOrModeratorOrAdminOrSuperuser, )

    def get_queryset(self) -> QuerySet:
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.select_related('review')
