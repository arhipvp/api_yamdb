from django.urls import include, path

from api.views import (AuthSignup, AuthToken, CategoryViewSet, CommentsViewSet,
                       GenresViewSet, ReviewsViewSet, TitleViewSet,
                       UsersViewSet)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('v1/genres', GenresViewSet)
router.register('v1/users', UsersViewSet, basename='users')
router.register('v1/titles', TitleViewSet)
router.register('v1/categories', CategoryViewSet)
router.register(
    'v1/titles/(?P<title_id>[0-9]+)/reviews',
    ReviewsViewSet,
    basename='reviews',
)
router.register(
    'v1/titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentsViewSet,
    basename='comments',
)

router.register('v1/categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('v1/auth/signup/', AuthSignup.as_view(), name='signup'),
    path('v1/auth/token/', AuthToken.as_view(), name='token'),
]
