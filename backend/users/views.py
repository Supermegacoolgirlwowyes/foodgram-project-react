from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.pagination import CustomPagination
from .models import Follow
from .serializers import FollowCreateSerializer, FollowDisplaySerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    pagination_class = CustomPagination


class FollowDisplayView(generics.ListAPIView):
    serializer_class = FollowDisplaySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return User.users.filtered(user).annotated(user).prefetched()


class FollowCreateView(views.APIView):
    queryset = Follow.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        data = {
            'follower': request.user.id,
            'following': user_id
        }
        serializer = FollowCreateSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        try:
            Follow.objects.get(
                follower=request.user,
                following=user_id
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Follow.DoesNotExist:
            return Response(
                data={'message': 'Вы не были подписаны на этого автора'},
                status=status.HTTP_400_BAD_REQUEST
            )
