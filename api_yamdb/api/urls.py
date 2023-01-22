from api.views import (AuthSignup, AuthToken, CommentsViewSet, GenresViewSet,
                       ReviewsViewSet, TitleViewSet, UsersViewSet,
                       СategoriesAPIDestroy, СategoriesAPIList)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('v1/genres', GenresViewSet)
router.register('v1/users', UsersViewSet, basename='users')
router.register('v1/titles', TitleViewSet)

router.register(
    'v1/titles/(?P<title_id>[0-9]+)/reviews',
    ReviewsViewSet,
    basename='Review',
)
router.register(
    'v1/titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentsViewSet,
    basename='Comment',
)


urlpatterns = [
    path('', include(router.urls)),
    path('v1/categories/', СategoriesAPIList.as_view()),
    path('v1/categories/<slug:slug>/', СategoriesAPIDestroy.as_view()),
    path('v1/auth/signup/', AuthSignup.as_view(), name='signup'),
    path('v1/auth/token/', AuthToken.as_view(), name='token'),
]
