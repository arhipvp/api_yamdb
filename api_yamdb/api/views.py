from rest_framework import viewsets
from rest_framework import filters
from django.shortcuts import get_object_or_404

from .models import Genres
from .serializers import GenresSerializer


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    lookup_field = 'slug'
