from django.core.mail import send_mail
from django.db.models import Avg, QuerySet
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title, User

from .filters import TitleFilter
from .permissions import (IsAdminOrReadOnly, IsAdminOrSuperUser,
                          IsAuthorOrModeratorOrAdminOrSuperuser,
                          IsSuperUserOrReadOnly)
from .serializers import (AuthSignupSerializer, AuthTokenSerializer,
                          CategorySerializer, CommentsSerializer,
                          GenresSerializer, ReviewsSerializer,
                          TitleSerializerCreate, TitleSerializerRead,
                          UsersSerializer)


class GenresViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet, ): 
    queryset = Genre.objects.all() 
    serializer_class = GenresSerializer 
    permission_classes = (IsAuthenticatedOrReadOnly, ) 
    filter_backends = (filters.SearchFilter,) 
    search_fields = ('name',) 
    lookup_field = 'slug' 

    def partial_update(self, request, slug=None): 
        if ( 
            request.user.is_user 
            or request.user.is_moderator 
            and request.method == 'PATCH' 
        ): 
            return Response(status=status.HTTP_403_FORBIDDEN) 
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED) 

    
    def destroy(self, request, *args, **kwargs): 
        if request.user.is_user or request.user.is_moderator: 
            return Response(status=status.HTTP_403_FORBIDDEN) 
        instance = self.get_object() 
        self.perform_destroy(instance) 
        return Response(status=status.HTTP_204_NO_CONTENT) 
 

    def create(self, request, *args, **kwargs): 
        if request.user.is_user or request.user.is_moderator: 
            return Response(status=status.HTTP_403_FORBIDDEN) 
        serializer = self.get_serializer(data=request.data) 
        serializer.is_valid(raise_exception=True) 
        self.perform_create(serializer) 
        headers = self.get_success_headers(serializer.data) 
        return Response(serializer.data, status=status.HTTP_201_CREATED, 
                        headers=headers) 


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(Avg('reviews__score')).order_by('id')
    serializer_class = TitleSerializerCreate
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'DELETE',):
            return TitleSerializerCreate
        return TitleSerializerRead

    def create(self, request, *args, **kwargs):
        if request.user.is_user or request.user.is_moderator:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def partial_update(self, request, *args, **kwargs):
        if request.user.is_user or request.user.is_moderator:
            return Response(status=status.HTTP_403_FORBIDDEN)
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.is_user or request.user.is_moderator:
            return Response(status=status.HTTP_403_FORBIDDEN)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,)

    def create(self, request, *args, **kwargs):
        if request.user.is_user or request.user.is_moderator:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def retrieve(self, request, slug=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        if request.user.is_user or request.user.is_moderator:
            return Response(status=status.HTTP_403_FORBIDDEN)
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
        url_path='me',
    )
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
    permission_classes = (IsAuthorOrModeratorOrAdminOrSuperuser,)
    
    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()
    
    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, id=self.kwargs.get('title_id'))
        )



class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = (IsAuthorOrModeratorOrAdminOrSuperuser,)

    def get_queryset(self) -> QuerySet:
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.select_related('review')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review = get_object_or_404(
                Review,
                id = self.kwargs.get('review_id'),
                title = self.kwargs.get('title_id'),
            )
        )