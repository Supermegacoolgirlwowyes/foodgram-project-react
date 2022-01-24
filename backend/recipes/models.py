from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):

    name = models.CharField(
        verbose_name='тег',
        max_length=50,
        unique=True,
        db_index=True,
    )
    color = models.CharField(
        verbose_name='цвет тега',
        max_length=7,
        unique=True,
        default="#ffffff",
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='название продукта',
        max_length=100,
    )
    measurement_unit = models.CharField(
        verbose_name='единица измерения',
        max_length=10,
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name + ", " + self.measurement_unit


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='название блюда',
        db_index=True,
        max_length=100
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор',
        related_name='recipes'
    )
    image = models.ImageField(
        upload_to='recipes',
        verbose_name='изображение'
    )
    text = models.TextField(
        verbose_name='описание приготовления',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        verbose_name='ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='теги',
        related_name='recipes',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='время приготовления (мин)',
        validators=[
            MinValueValidator(
                1,
                message='Круглый ноль такой хорошенький, '
                        'Но не значит ничегошеньки!'
            )
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='дата публикации',
        auto_now_add=True,
    )

    def list_ingredients(self):
        return ', '.join([i.name for i in self.ingredients.all()])

    def list_tags(self):
        return ', '.join([t.name for t in self.tags.all()])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-pub_date']
        unique_together = ('author', 'name')


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.PROTECT, verbose_name='ингредиент'
    )
    amount = models.PositiveIntegerField(
        verbose_name='количество',
        validators=[
            MinValueValidator(
                1,
                message='Из ноля каши не сваришь!'
            )
        ]
    )

    class Meta:
        ordering = ['recipe']
        unique_together = ('recipe', 'ingredient')


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='is_favorited'
    )

    class Meta:
        ordering = ['user']
        unique_together = ('user', 'recipe')


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='buyer'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='is_in_shopping_cart'
    )

    class Meta:
        ordering = ['user']
        unique_together = ('user', 'recipe')
