from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import GenresViewSet, AuthToken, AuthSignup, UsersViewSet

router = DefaultRouter()
router.register('v1/genres', GenresViewSet)
router.register('v1/users', UsersViewSet, basename='users')
urlpatterns = [
    path('', include(router.urls)),
    path('v1/auth/signup/', AuthSignup.as_view(), name='signup'),
    path('v1/auth/token/', AuthToken.as_view(), name='token'),

]
