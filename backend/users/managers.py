from django.contrib.auth.models import BaseUserManager
from django.db.models import Count, Exists, OuterRef, QuerySet

from . import models


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        user = self.model(
            email=email,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class SubscriptionQuerySet(QuerySet):
    def filtered(self, user):
        return self.filter(following__follower=user)

    def annotated(self, user):
        return self.annotate(
            recipes_count=Count('recipes')
        ).annotate(
            is_subscribed=Exists(
                models.Follow.objects.filter(
                    follower=user,
                    following=OuterRef('pk')
                )
            )
        )

    def prefetched(self):
        return self.prefetch_related('recipes').all()
