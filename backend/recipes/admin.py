from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug', )
    search_fields = ('id', 'name', 'slug', )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit', )
    list_filter = ('name', )
    search_fields = ('id', 'name', )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'author', 'list_ingredients',
        'list_tags', 'count_favorites'
    )
    list_filter = ('author', 'name', 'tags', )
    search_fields = (
        'name', 'author__username', 'ingredients__name', 'tags__name'
    )

    def list_ingredients(self, obj):
        return ', '.join([i.name for i in obj.ingredients.all()])

    def list_tags(self, obj):
        return ', '.join([t.name for t in obj.tags.all()])

    def count_favorites(self, obj):
        return obj.is_favorited.count()


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount', )
    search_fields = ('recipe__name', 'ingredient__name', )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
