from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import DatabaseError, models, transaction
from django.utils.translation import gettext as _

from .managers import RecipeQuerySet

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
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
    )

    class Meta:
        ordering = ['name']
        verbose_name = _('тег')
        verbose_name_plural = _('теги')

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
        ordering = ['name']
        verbose_name = _('ингредиент')
        verbose_name_plural = _('ингредиенты')

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


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
    tags = models.ManyToManyField(
        Tag,
        verbose_name='теги',
        related_name='recipes',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='время приготовления (мин)',
        null=True,
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

    objects = RecipeQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-pub_date']
        verbose_name = _('рецепт')
        verbose_name_plural = _('рецепты')
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'name'],
                name="author and recipe name not unique"
            )
        ]

    @staticmethod
    def get_tags_ingredients(**data):
        tags = data.pop('tags')
        ingredients = data.pop('ingredients')
        return tags, ingredients, data

    @staticmethod
    def add_ingredients(recipe, ingredients):
        for i in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=i['id'],
                amount=i['amount']
            )
        return

    @classmethod
    def create(cls, author, **data):
        tags, ingredients, data = cls.get_tags_ingredients(**data)
        try:
            with transaction.atomic():
                recipe = cls(
                    author=author, **data)
                recipe.save()
                cls.add_ingredients(recipe, ingredients)
                recipe.tags.set(tags)
                recipe.is_favorited = False
                recipe.is_in_shopping_cart = False
                return recipe
        except DatabaseError:
            cls.handle_exception()

    def update(self, **data):
        tags, ingredients, data = self.get_tags_ingredients(**data)
        for field, value in data.items():
            setattr(self, field, value)
        RecipeIngredient.objects.filter(recipe=self).delete()
        self.add_ingredients(self, ingredients)
        self.save()
        self.tags.clear()
        self.tags.set(tags)
        return self


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт',
        related_name='ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        verbose_name='ингредиент'
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
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name="recipe and ingredient not unique"
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorited_by',
        verbose_name='пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorited',
        verbose_name='рецепт'
    )

    class Meta:
        ordering = ['user']
        verbose_name = _('избранное')
        verbose_name_plural = _('избранное')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name="user and favorite recipe not unique"
            )
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='buyer',
        verbose_name='пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт'
    )

    class Meta:
        ordering = ['user']
        verbose_name = _('список покупок')
        verbose_name_plural = _('список покупок')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name="user and recipe in shopping cart not unique"
            )
        ]
