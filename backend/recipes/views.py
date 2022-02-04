import io

from django.db.models import Exists, OuterRef, Sum
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import get_object_or_404
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
    search_fields = ['name']


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = [CreateOrAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return Recipe.objects.annotated(user).prefetched(user)

    def get_serializer_class(self):
        if self.request.method in ['list', 'retrieve']:
            return RecipeDisplaySerializer
        return RecipeCreateSerializer

    @staticmethod
    def post_method(request, recipe_id, serializers):
        data = {'user': request.user.id, 'recipe': recipe_id}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method(request, recipe_id, model):
        user = request.user
        instance = get_object_or_404(model, user=user, recipe_id=recipe_id)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        return self.post_method(
            request, pk, FavoriteSerializer
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_method(
            request, pk, Favorite
        )

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        return self.post_method(
            request, pk, ShoppingCartSerializer
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_method(
            request, pk, ShoppingCart
        )


def create_pdf(ingredients):
    x, y = 50, 770
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    pdfmetrics.registerFont(
        ttfonts.TTFont('Bitter', 'data/Bitter-VariableFont.ttf')
    )
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
    ingredients = RecipeIngredient.objects.annotate(
        is_in_shopping_cart=Exists(
            ShoppingCart.objects.filter(
                user=request.user, recipe=OuterRef('recipe__pk')
            )
        )
    ).filter(
        is_in_shopping_cart=True
    ).values(
        'ingredient__name', 'ingredient__measurement_unit',
    ).order_by(
        'ingredient__name'
    ).annotate(amount=Sum('amount'))
    return create_pdf(ingredients)
