from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, ValidationError

from recipes.models import Recipe
from .models import Follow

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'username', 'first_name', 'last_name', 'password'
        )


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return (user.is_authenticated and
                user.follower.filter(following=obj).exists())


class FollowRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowDisplaySerializer(serializers.ModelSerializer):
    is_subscribed = serializers.BooleanField()
    recipes = FollowRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')


class FollowCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ('follower', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('follower', 'following'),
                message='Вы уже подписаны на этого автора'
            )
        ]

    def validate_following(self, following):
        request = self.context['request']
        follower = request.user
        if following == follower:
            raise ValidationError('Вы не можете подписаться на самого себя')
        return following

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return FollowDisplaySerializer(
            instance.following, context=context
        ).data
