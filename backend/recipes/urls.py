from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet, shopping_list

router = DefaultRouter()
router.register('', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('download_shopping_cart/', shopping_list),
    path('', include(router.urls)),
]
