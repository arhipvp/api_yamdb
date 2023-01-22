from django.core.mail import send_mail
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Categories, Comment, Genres, Review, Title, User

from .permissions import IsAdminOrReadOnly, IsAdminOrSuperUser
from .serializers import (AuthSignupSerializer, AuthTokenSerializer,
                          CategoriesSerializer, CommentsSerializer,
                          GenresSerializer, ReadOnlyTitleSerializer,
                          ReviewsSerializer, TitleSerializer, UsersSerializer)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )



class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAuthenticatedOrReadOnly,)
    
    def retrieve(self, request, slug=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def partial_update(self, request, slug=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class AuthSignup(APIView):
    """
    Зарегистрироваmь пользователя и отправить ему код подтверждения на email
    """

    @staticmethod
    def post(request):
        serializer = AuthSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = User.objects.get_or_create(
            username=serializer.data['username'], email=serializer.data['email']
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

    def get_title(self, request: HttpRequest) -> Title:
        del request
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self) -> QuerySet:
        return self.get_title(self).reviews.select_related('title')


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer

    def get_review(self, request: HttpRequest) -> Title:
        del request
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self) -> QuerySet:
        return self.get_review(self).comments.select_related('review')
