from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FollowAPIView


urlpatterns = [
    path('users/subscriptions/', FollowAPIView.as_view(), name='subscriptions'),
    path('', include('djoser.urls'))
    ]
