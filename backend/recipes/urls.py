from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FavoriteView, IngredientViewSet, RecipeViewSet, ShoppingCartView, ShoppingCartDisplayView, ShoppingList, TagViewSet

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path(
        'recipes/<int:recipe_id>/favorite/',
        FavoriteView.as_view(),
        name='favorite'
    ),
    path(
        'recipes/<int:recipe_id>/shopping_cart/',
        ShoppingCartView.as_view(),
        name='shopping cart'
    ),
    path('', include(router.urls)),
]
