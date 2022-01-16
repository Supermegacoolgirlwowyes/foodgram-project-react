from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FavoriteViewSet, IngredientViewSet, RecipeViewSet, TagViewSet

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet, basename='recipes')
# router.register('recipes/<id:id>', RecipeRetrieveViewset, basename='recipes')


urlpatterns = [
    path('', include(router.urls)),
]

# path('recipes/<int:id>/favorite/', FavoriteViewSet),
