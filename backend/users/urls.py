from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FollowDisplayView, FollowCreateView


urlpatterns = [
    path('users/subscriptions/', FollowDisplayView.as_view(), name='subscriptions'),
    path('users/<int:user_id>/subscribe/', FollowCreateView.as_view(), name='subscribe'),
    path('', include('djoser.urls'))
    ]
