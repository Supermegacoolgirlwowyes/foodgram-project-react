from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.utils.timezone import now
from rest_framework import generics, mixins, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404 as _get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from djoser import permissions, signals, utils
from djoser.compat import get_user_email
from djoser.conf import settings
from djoser.views import UserViewSet

from .models import Follow
from .serializers import CustomUserSerializer, FollowDisplaySerializer
from recipes.pagination import CustomPagination

User = get_user_model()


class FollowAPIView(generics.ListAPIView):
    serializer_class = FollowDisplaySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return User.objects.filter(following__follower=self.request.user)


    """def perform_create(self, serializer):
        is_subscribed = _get_object_or_404(User, id=self.kwargs.get('id'))
        if is_subscribed != self.request.user:
            serializer.save(is_subscribed=is_subscribed, user=self.request.user)"""
