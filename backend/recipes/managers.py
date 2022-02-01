from django.contrib.auth import get_user_model
from django.db.models import (Count, Exists, Manager, OuterRef, Prefetch,
                              QuerySet)

from users.models import Follow
from . import models

User = get_user_model()


class RecipeQuerySet(QuerySet):

    def annotated(self, user):
        if not user.is_authenticated:
            return self.annotate(
                is_favorited=Count(0),
                is_in_shopping_cart=Count(0)
            )
        return self.annotate(
            is_favorited=Exists(
                models.Favorite.objects.filter(
                    recipe=OuterRef('pk'),
                    user=user
                )
            ),
            is_in_shopping_cart=Exists(
                models.ShoppingCart.objects.filter(
                    recipe=OuterRef('pk'),
                    user=user
                )
            )
        )

    def prefetched(self, user):
        if not user.is_authenticated:
            return self.prefetch_related(
                Prefetch(
                    'author',
                    User.objects.annotate(
                        is_subscribed=Count(0)
                    )
                )
            )
        return self.prefetch_related(
            Prefetch(
                'author',
                User.objects.annotate(
                    is_subscribed=Exists(
                        Follow.objects.filter(
                            follower=user,
                            following=OuterRef('pk')
                        )
                    )
                )
            )
        )


class RecipeManager(Manager):

    def get_queryset(self):
        return RecipeQuerySet(self.model, using=self._db)

    def annotated(self, user):
        return self.get_queryset().annotated(user)

    def prefetched(self, user):
        return self.get_queryset().prefetched(user)
