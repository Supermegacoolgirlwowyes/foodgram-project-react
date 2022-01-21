import io

from django.db.models import Sum
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, views, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404  # as _get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)
from .pagination import CustomPagination
from .permissions import CreateOrAuthorOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeDisplaySerializer,
                          ShoppingCartSerializer, TagSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = [AllowAny]
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [AllowAny]
    serializer_class = IngredientSerializer
    filter_backends = [IngredientFilter, ]
    search_fields = ['^name']


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [CreateOrAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method in ['list', 'retrieve']:
            return RecipeDisplaySerializer
        return RecipeCreateSerializer


class FavoriteView(views.APIView):
    queryset = Favorite.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, recipe_id):
        data = {
            'user': request.user.id,
            'recipe': get_object_or_404(Recipe, id=recipe_id).id
        }
        serializer = FavoriteSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        try:
            Favorite.objects.get(
                user=request.user,
                recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return Response(
                data={'message': 'Этого рецепта не было в избранном'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ShoppingCartView(views.APIView):
    queryset = ShoppingCart.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, recipe_id):
        data = {
            'user': request.user.id,
            'recipe': get_object_or_404(Recipe, id=recipe_id).id
        }
        serializer = ShoppingCartSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        try:
            ShoppingCart.objects.get(
                user=request.user,
                recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ShoppingCart.DoesNotExist:
            return Response(
                data={'message': 'Этого рецепта не было в списке покупок'},
                status=status.HTTP_400_BAD_REQUEST
            )


def some_view(ingredients):
    x, y = 50, 770
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont('Bitter', 'data/Bitter-VariableFont.ttf'))
    pdf.setTitle('Список_покупок')
    pdf.setFont('Bitter', 16)
    pdf.drawString(x, y, 'Cписок покупок')
    y -= 30
    pdf.setFont('Bitter', 12)
    for i in ingredients:
        pdf.drawString(
            x,
            y,
            f'{i["ingredient__name"]} - {i["amount"]}'
            f' {i["ingredient__measurement_unit"]}'
        )
        y -= 20
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return FileResponse(
        buffer,
        as_attachment=True,
        filename='Shopping_list.pdf'
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def shopping_list(request):
    ingredients = RecipeIngredient.objects.filter(
        recipe__is_in_shopping_cart__user=request.user
    ).values(
        'ingredient__name', 'ingredient__measurement_unit',
    ).order_by(
        'ingredient__name'
    ).annotate(amount=Sum('amount'))
    return some_view(ingredients)
