from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from recipes.views import IngredientViewSet, TagViewSet

router = DefaultRouter()

router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/recipes/', include('recipes.urls')),
    path('api/users/', include('users.urls')),
    path('api/', include(router.urls)),
]
