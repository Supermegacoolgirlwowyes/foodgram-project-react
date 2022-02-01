from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Follow

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'first_name', 'last_name', 'email', )
    list_display_links = ('username', )
    search_fields = ('pk', 'username', 'first_name', 'last_name', 'email', )
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'following', )
    list_display_links = ('follower',)
    search_fields = ('follower', 'following', )
    empty_value_display = '-пусто-'
