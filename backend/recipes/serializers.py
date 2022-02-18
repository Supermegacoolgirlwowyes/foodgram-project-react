from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, validators

from users.serializers import CustomUserSerializer
from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения одного или всех тегов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug', )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения одного или несольких ингредиентов."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения ингредиентов в рецепте."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount', )


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Cериализатор для добавления ингредиентов при создании рецепта."""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount', )


class RecipeDisplaySerializer(serializers.ModelSerializer):
    """Cериализатор для отображения одного или нескольких рецептов."""
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(read_only=True, many=True)
    is_favorited = serializers.BooleanField()
    is_in_shopping_cart = serializers.BooleanField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
        )


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Cериализатор для создания и редактирования рецепта."""
    ingredients = IngredientAmountSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time', )

    def validate_ingredients(self, ingredients):
        if self.context.get('request').method in ['POST', 'PUT', 'PATCH']:
            ingredient_id_list = []
            for i in ingredients:
                if i['id'] in ingredient_id_list:
                    raise validators.ValidationError(
                        {'ingredients': 'Ингредиенты должны быть уникальными'}
                    )
                if i['amount'] < 1:
                    raise validators.ValidationError(
                        {'amount': 'Значение должно быть больше ноля'}
                    )
                ingredient_id_list.append(i['id'])
        return ingredients

    def validate_name(self, name):
        request = self.context.get('request')
        if request.method == 'POST':
            user = request.user
            if Recipe.objects.filter(author=user, name=name).exists():
                raise validators.ValidationError(
                    'Рецепт с таким названием у вас уже есть'
                )
        return name

    def create(self, validated_data):
        user = self.context.get('request').user
        return Recipe.create(user, **validated_data)

    def update(self, instance, validated_data):
        return instance.update(**validated_data)
        # return Recipe.update(instance, **validated_data)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeDisplaySerializer(instance, context=context).data


class RecipePreviewSerializer(serializers.ModelSerializer):
    """Cериализатор для превью рецепта."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteShoppingSerializer(serializers.ModelSerializer):
    """Cериализатор родитель для Favorite и ShoppingCart."""
    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipePreviewSerializer(instance.recipe, context=context).data

    class Meta:
        fields = ('user', 'recipe',)


class FavoriteSerializer(FavoriteShoppingSerializer):
    """Cериализатор для добавления рецепта в избранное."""

    class Meta(FavoriteShoppingSerializer.Meta):
        model = Favorite
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'recipe'],
                message='Вы уже добавили этот рецепт в избранное'
            )
        ]


class ShoppingCartSerializer(FavoriteShoppingSerializer):
    """Cериализатор для добавления рецепта в список покупок."""
    class Meta(FavoriteShoppingSerializer.Meta):
        model = ShoppingCart
        validators = [
            validators.UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=['user', 'recipe'],
                message='Вы уже добавили этот рецепт в список покупок'
            )
        ]
