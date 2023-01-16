from rest_framework import viewsets

from .models import Genres
from .serializers import GenresSerializer


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
