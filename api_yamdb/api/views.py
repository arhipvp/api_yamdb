from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Genres, Title, User, Сategories
from rest_framework.decorators import action
from .serializers import (AuthSignupSerializer, AuthTokenSerializer,
                          GenresSerializer, TitleSerializer, UsersSerializer,
                          СategoriesSerializer)

from .permissions import IsAdminOrReadOnly

class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    lookup_field = 'slug'
    
    

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    
    
class СategoriesViewSet(viewsets.ModelViewSet):
    queryset = Сategories.objects.all()
    serializer_class = СategoriesSerializer
    search_fields = 'name'
    lookup_field = 'slug'
    permission_classes = (IsAuthenticatedOrReadOnly, )


        

    

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
