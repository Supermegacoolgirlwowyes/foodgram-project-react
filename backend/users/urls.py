from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SubscriptionViewSet


urlpatterns = [
    path('users/subscriptions/', SubscriptionViewSet, name='subscriptions'),
    path('', include('djoser.urls'))
    ]
