from drf_extra_fields.fields import Base64ImageField

from rest_framework import serializers, validators

from .models import Favorite, Ingredient, Recipe, RecipeIngredient, ShoppingCart, Tag
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):
    """ Сериализатор для отображения одного или всех тегов """
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug', )


class IngredientSerializer(serializers.ModelSerializer):
    """ Сериализатор для отображения одного или несольких ингредиентов """
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """ Сериализатор для отображения ингредиентов в рецепте """
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount', )


class IngredientAmountSerializer(serializers.ModelSerializer):
    """ Cериализатор для добавления ингредиентов при создании рецепта """
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount', )


class RecipeDisplaySerializer(serializers.ModelSerializer):
    """ Cериализатор для отображения одного или нескольких рецептов """
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time',
        )

    def get_ingredients(self, recipe):
        ingredients = RecipeIngredient.objects.filter(recipe=recipe)
        return RecipeIngredientSerializer(ingredients, many=True).data

    def get_is_favorited(self, recipe):
        user = self.context.get('request').user
        if user.is_authenticated and user.favorited_by.filter(recipe=recipe):
            return True
        return False

    def get_is_in_shopping_cart(self, recipe):
        user = self.context.get('request').user
        if user.is_authenticated and user.buyer.filter(recipe=recipe):
            return True
        return False


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = IngredientAmountSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'tags', 'image', 'name',
                  'text', 'cooking_time', )

    def validate_ingredients(self, ingredients):
        if self.context.get('request').method in ['POST', 'PUT', 'PATCH']:
            ingredient_id_list = []
            for i in ingredients:
                if i['id'] in ingredient_id_list:
                    raise validators.ValidationError('Не стоит добавлять два одинаковых ингредиента')
                if i['amount'] < 1:
                    raise validators.ValidationError('Что-то как-то мало')
                ingredient_id_list.append(i['id'])
        return ingredients

    def validate_name(self, name):
        request = self.context.get('request')
        if request.method in ['POST', 'PUT', 'PATCH']:
            user = request.user
            if Recipe.objects.filter(author=user, name=name).exists():
                raise validators.ValidationError('Рецепт с таким названием у вас уже есть')
        return name

    def add_tags(self, tags, recipe):
        for tag in tags:
            recipe.tags.add(tag)

    def add_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount'],
            )

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.add_ingredients(ingredients, recipe)
        self.add_tags(tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.get('tags')
        ingredients = validated_data.get('ingredients')
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        self.add_tags(tags, instance)
        RecipeIngredient.objects.filter(recipe=instance).delete()
        self.add_ingredients(ingredients, instance)
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeDisplaySerializer(instance, context=context).data


class RecipePreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('user', 'recipe', )
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'recipe'],
                message='Вы уже добавили этот рецепт в избранное'
            )
        ]

    """def validate_following(self, following):
        request = self.context['request']
        follower = request.user
        if following == follower:
            raise ValidationError('Вы не можете подписаться на самого себя')
        return following"""

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipePreviewSerializer(instance.recipe, context=context).data


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe', )
        validators = [
            validators.UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=['user', 'recipe'],
                message='Вы уже добавили этот рецепт в избранное'
            )
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipePreviewSerializer(instance.recipe, context=context).data
