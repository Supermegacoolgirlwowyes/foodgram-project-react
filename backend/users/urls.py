from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, FollowCreateView, FollowDisplayView

router = DefaultRouter()
router.register('', CustomUserViewSet)


urlpatterns = [
    path(
        'subscriptions/',
        FollowDisplayView.as_view(),
        name='subscriptions'
    ),
    path(
        '<int:user_id>/subscribe/',
        FollowCreateView.as_view(),
        name='subscribe'
    ),
    path('', include(router.urls))
]
