from django.core.mail import send_mail
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets, generics
from rest_framework.decorators import action
from rest_framework.permissions import (IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Comment, Genres, Review, Title, User, Сategories

from .permissions import IsAdminOrReadOnly, IsAdminOnly
from .serializers import (AuthSignupSerializer, AuthTokenSerializer,
                          CommentsSerializer, GenresSerializer,
                          ReadOnlyTitleSerializer, ReviewsSerializer,
                          TitleSerializer, UsersSerializer,
                          СategoriesSerializer)
from rest_framework import generics, mixins, views
from rest_framework.generics import ListCreateAPIView, UpdateAPIView

class СategoriesAPIList(ListCreateAPIView, UpdateAPIView):
    queryset = Сategories.objects.all()
    serializer_class = СategoriesSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly, )
    #http_method_names = ['get', 'post', , 'head', 'options', ]	
    
    
class СategoriesAPIDestroy(generics.DestroyAPIView):
    queryset = Сategories.objects.all()
    serializer_class = СategoriesSerializer
    lookup_field = 'slug'
    http_method_names = ['delete', 'head', 'options', ]
    permission_classes = (IsAdminOnly, IsAuthenticated)

class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return ReadOnlyTitleSerializer
        return TitleSerializer
    
    
    



    


class AuthSignup(APIView):
    """
    Зарегистрироваmь пользователя и отправить ему код подтверждения на email
    """

    @staticmethod
    def post(request):
        serializer = AuthSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
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
    permission_classes = (IsAuthenticated,)
    lookup_field = 'username'


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
