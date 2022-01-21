from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavoriteView, IngredientViewSet, RecipeViewSet,
                    ShoppingCartView, TagViewSet, shopping_list)

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path(
        '<int:recipe_id>/favorite/',
        FavoriteView.as_view(),
        name='favorite'
    ),
    path(
        '<int:recipe_id>/shopping_cart/',
        ShoppingCartView.as_view(),
        name='shopping cart'
    ),
    path('download_shopping_cart/', shopping_list),
    path('', include(router.urls)),
]
