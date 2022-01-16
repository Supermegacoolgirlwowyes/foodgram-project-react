from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Follow

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'first_name', 'last_name', 'email', )
    search_fields = ('pk', 'username', 'first_name', 'last_name', 'email', )
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'follower', 'following', )
    search_fields = ('follower', 'following', )
    empty_value_display = '-пусто-'

admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
