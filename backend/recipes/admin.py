from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug', )
    list_display_links = ('name', )
    search_fields = ('id', 'name', 'slug', )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit', )
    list_display_links = ('name', )
    list_filter = ('name', )
    search_fields = ('id', 'name', )


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    min_num = 3
    extra = 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj=None, **kwargs)
        formset.validate_min = True
        return formset


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'author', 'list_ingredients',
        'list_tags', 'count_favorites'
    )
    list_display_links = ('name', )
    list_filter = ('author', 'name', 'tags', )
    search_fields = (
        'name', 'author__username', 'ingredients__name', 'tags__name'
    )
    inlines = [RecipeIngredientInline, ]

    def list_ingredients(self, obj):
        return ', '.join(i.ingredient.name for i in obj.ingredients.all())
    list_ingredients.short_description = 'ингредиенты'

    def list_tags(self, obj):
        return ', '.join([t.name for t in obj.tags.all()])
    list_tags.short_description = 'теги'

    def count_favorites(self, obj):
        return obj.favorited.count()
    count_favorites.short_description = 'в избранном'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_display_links = ('user', )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_display_links = ('user', )
