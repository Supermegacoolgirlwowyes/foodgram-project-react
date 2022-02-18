from django.contrib.auth import get_user_model
from django.db.models import Count, Exists, OuterRef, Prefetch, QuerySet, Value

from users.models import Follow
from . import models

User = get_user_model()


class RecipeQuerySet(QuerySet):

    def annotated(self, user):
        if not user.is_authenticated:
            return self.annotate(
                is_favorited=Value(0),
                is_in_shopping_cart=Value(0)
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
