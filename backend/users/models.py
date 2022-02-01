from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext as _

from users.managers import CustomUserManager, SubscriptionQuerySet


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='адрес электронной почты',
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        verbose_name='уникальный юзернейм',
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='имя',
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='фамилия',
        max_length=150,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', ]

    objects = CustomUserManager()
    users = SubscriptionQuerySet.as_manager()

    class Meta:
        ordering = ['id', ]
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')

    def __str__(self):
        return self.username


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='подписчик'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='автор'
    )

    class Meta:
        ordering = ['follower']
        verbose_name = _('подписка')
        verbose_name_plural = _('подписки')
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'following'],
                name="follower and following are not unique"
            )
        ]

    def __str__(self):
        return (f'{self.follower.username} подписан на '
                f'{self.following.username}.')
