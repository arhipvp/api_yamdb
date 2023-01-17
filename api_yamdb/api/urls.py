from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import GenresViewSet

router = DefaultRouter()
router.register('v1/genres', GenresViewSet)

urlpatterns = [
    path('', include(router.urls)),
]