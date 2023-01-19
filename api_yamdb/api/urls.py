from api.views import AuthSignup, AuthToken, СategoriesViewSet, GenresViewSet, UsersViewSet, TitleViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('v1/genres', GenresViewSet)
router.register('v1/users', UsersViewSet, basename='users')
router.register('v1/titles', TitleViewSet)
router.register('v1/categories', СategoriesViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('v1/auth/signup/', AuthSignup.as_view(), name='signup'),
    path('v1/auth/token/', AuthToken.as_view(), name='token'),
]
